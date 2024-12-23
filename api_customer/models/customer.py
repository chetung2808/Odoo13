import base64
import requests
from PIL import Image
from io import BytesIO
import logging
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import binascii

_logger = logging.getLogger(__name__)

class PartnerAPI(models.Model):
    _inherit = "res.partner"

    external_user_id = fields.Integer(string="External User ID", readonly=True)
    avatar_url = fields.Char(string="Avatar URL", readonly=True)
    image_1920 = fields.Binary(string="Image 1920")  # Adding the image field to store the image

    def _fetch_image_as_binary(self, image_url):
        """Fetch and validate an image from a URL."""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()


            # Check if the content type is an image
            if 'image' not in response.headers.get('Content-Type', ''):
                _logger.warning(f"URL does not return an image: {image_url}")
                return False


            # Validate and encode the image
            image = Image.open(BytesIO(response.content))
            image.verify()  # Check if it's a valid image
            binary_data = base64.b64encode(response.content).decode('utf-8')  # Encode to Base64
            return binary_data
        except (requests.exceptions.RequestException, OSError) as e:
            _logger.warning(f"Failed to fetch or decode image from {image_url}: {e}")
            return False

    def is_valid_base64(self, data):
        """Check if the data is valid Base64."""
        try:
            base64.b64decode(data, validate=True)
            return True
        except binascii.Error:
            return False

    def fix_base64_padding(self, data):
        """Fix Base64 padding if necessary."""
        return data + '=' * (-len(data) % 4)

    def action_fetch_api_data(self):
        """Fetch data from the ReqRes API and update res.partner records."""
        api_url = 'https://dummyjson.com/users'
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            for user in data.get('users', []):
                # Define a default phone number
                default_phone = "000-000-0000"

                # Check if a partner already exists with the external ID
                partner = self.search([('external_user_id', '=', user['id'])], limit=1)
                if not partner:
                    # Create a new partner record
                    avatar_data = self._fetch_image_as_binary(user['image'])
                    if avatar_data:
                        avatar_data = self.fix_base64_padding(avatar_data)
                        if self.is_valid_base64(avatar_data):
                            partner = self.create({
                                'name': f"{user['firstName']} {user['lastName']} {user['maidenName']}",
                                'external_user_id': user['id'],
                                'avatar_url': user['image'],
                                'image_1920': avatar_data,  # Store the image in the image_1920 field
                                'email': user['email'],
                                'phone': user['phone'] or default_phone,  # Use default phone value if none exists
                            })
                else:
                    # Update the existing partner record
                    avatar_data = self._fetch_image_as_binary(user['image'])
                    if avatar_data:
                        avatar_data = self.fix_base64_padding(avatar_data)
                        if self.is_valid_base64(avatar_data):
                            partner.write({
                                'name': f"{user['firstName']} {user['lastName']} {user['maidenName']}",
                                'avatar_url': user['image'],
                                'image_1920': avatar_data,  # Update the image field
                                'email': user['email'],
                                'phone': user['phone'] or default_phone,  # Keep phone or use default
                            })
        except requests.exceptions.RequestException as e:
            raise Warning(_("Error fetching data from API: %s") % e)
