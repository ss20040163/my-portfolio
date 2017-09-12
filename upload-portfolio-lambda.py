

# Import the modules required for the script to operate.
import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

# Setting the S3 Security mode. AWS Code Build uses Server Side Encryption by default.
# Therefore any files it places on the platform will be encrypted. We need to be ready for it.

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

# Tell the script where our main production bucket is
portfolio_bucket = s3.Bucket('portfolio.ss20040163-serverless.co.uk')

#Tell the script where our Dev Bucket is.
build_bucket = s3.Bucket('portfoliobuild.ss20040163-serverless.co.uk')

#Create a resource to hold the content being sent to memory for unpacking
portfolio_zip = StringIO.StringIO()

# Create a resource that downloads the file from the dev bucket, and populates it into the IN-Memory
# SttringIO Holder, ready for unp
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

# Upload the files to the production bucket.

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
		obj = myzip.open(nm)
		portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
		portfolio_bucket.Object(nm).Acl().put(ACL='public-read')


## The permissions will be wrong after the upload, so you need to change them to public read.
