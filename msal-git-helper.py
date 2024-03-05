# Given the client ID and tenant ID for an app registered in Azure,
# provide a <ms-entra-id> access token and a refresh token.

# If the caller is not already signed in to Azure, the caller's
# web browser will prompt the caller to sign in first.

# pip install msal
from msal import PublicClientApplication
import sys

# You can hard-code the registered app's client ID and tenant ID here,
# or you can provide them as command-line arguments to this script.
client_id = '<client-id>'
tenant_id = '<tenant-id>'

# Do not modify this variable. It represents the programmatic ID for
# Azure Databricks along with the default scope of '/.default'.
scopes = [ 'email', 'User.Read' ]  # MSAL expects a list of strings, and "openid" is used by default

# Check for too few or too many command-line arguments.
if (len(sys.argv) > 1) and (len(sys.argv) != 3):
  print("Usage: msal-git-helper.py <client ID> <tenant ID>")
  exit(1)

# If the registered app's client ID and tenant ID are provided as
# command-line variables, set them here.
if len(sys.argv) > 1:
  client_id = sys.argv[1]
  tenant_id = sys.argv[2]

## This is a one-off script. The default in-memory token cache would work just fine
#cache = SerializableTokenCache()

app = PublicClientApplication(
  client_id = client_id,
  authority = "https://login.microsoftonline.com/" + tenant_id,
  #token_cache = cache
)

acquire_tokens_result = app.acquire_token_interactive(
  scopes = scopes
)

if 'id_token' in acquire_tokens_result:
  print(acquire_tokens_result["id_token"], end='')
else:
  print("Error: " + acquire_tokens_result.get('error', "unknown"), file=sys.stderr)
  print("Description: " + acquire_tokens_result.get('error_description', "n/a"), file=sys.stderr)
