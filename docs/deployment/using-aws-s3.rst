###################################
Using AWS S3 or Other Cloud Storage
###################################

By the time you are in a production environment, you will have configured Arches
with a web server, such as Apache or nginx.  While you need a web server to
serve the app itself, there are two pieces of the app that can be separated from
the web server and served independently. These are the 'static' files (the css,
javascript, and logos that are used throughout the app) and the 'media' files
(any user uploaded files, such as images or documents).


Why Use Cloud Storage (Like S3) with Arches?
============================================

These static and media files need to be stored someplace accessible via Web (HTTP) requests
made by Arches users. Many of the existing tutorials on this matter are concerned with serving both
static and media files, because the more load you can take off of your web server
the better. However, for the purposes of this tutorial, we are only dealing with
media files. S3 (and other cloud storage services!) are especially suited to storing
a large (and growing) amount of files. For instance:

+ Cloud storage is cheap: As per the `S3 price chart <http://aws.amazon.com/s3/pricing/>`_, it costs just $.03 per gb/month.  So a database with 10gb of photos will have a media storage cost of $3/month, plus a small amount per transaction ($0.004 per 10,000 GET requests, e.g.). `Google Cloud storage <https://cloud.google.com/storage/pricing>`_ has similar costs, as does `Azure Cloud storage <https://azure.microsoft.com/en-us/pricing/details/storage/blobs>`_.
+ Cloud storage is scalable: You only pay for the amount of data you have stored, and you have no real limit on how much you can store.  This allows for an Arches deployment on a small server, either in-house or a small cloud instance (AWS EC2, Google, DigitalOcean, etc.) to store hundreds of gigabytes of media--photos, audio, video, documents--without having to restructure to accommodate more data.

You should be able to use Cloud storage regardless of where your app is hosted, whether on an internal server, an AWS EC2 instance, a DigitalOcean droplet, etc.

.. note::
    We provide specific guidance for integrating Arches with Amazon S3 storage because it is currently popular and familiar to many. However, we want to emphasize that you can choose among different commercial cloud storage services to use with Arches. The S3 integration steps below will give you a general picture on how to use other cloud storage services, but you'll need to change some specifics. Please refer to `django-storages documentation <https://django-storages.readthedocs.io/en/latest/index.html>`_ for additional help on integrating with different cloud storage providers.


.. note::

  We've found that by following the steps below, deleting an Information Resource
  from within Arches will *not* automatically remove the file from your S3 bucket.
  You can manually delete files from the bucket for now, or the intrepid developer
  may check out the answer to `this question <https://groups.google.com/forum/#!topic/archesproject/QHKqMISRkV8>`_ on the Arches forum.


Steps to Follow
===============

To use S3, you will need an AWS account, which is just an extension of a normal
Amazon account. `Here's <http://aws.amazon.com/getting-started/>`_ some
information on how to get started.


Having worked through a number of existing tutorials (mostly
`dylanbfox.blogspot.com <http://dylanbfox.blogspot.com/2015/01/using-s3-to-serve-and-store-your-django.html>`_,
`www.caktusgroup.com <https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files>`_,
and `www.holovaty.com <http://www.holovaty.com/writing/amazon-s3-media/>`_),
we've distilled these steps to show how you can use S3 in conjunction with your Arches
app.  Before beginning, you will need to have set up and logged into your AWS account.

1. Create credentials for your Arches app

    These new credentials will allow your Arches app to access the S3 bucket.

    1. Access the AWS Identity and Access Management (IAM) Console.
    2. Create a new user (named something like "arches_media"), and download the new credentials.  This will be a small .csv file that includes an Access Key ID and a Secret Key.
    3. Also, go to the new user's properties, and record the User ARN.

2. Create a new bucket on S3

    Next, you'll need to create a new bucket and give it the appropriate settings.

    1. Create a bucket, named something like "my_app-media".
    2. In the new bucket properties, under Permissions, create a new bucket policy
    3. Paste the following text into your new policy, inserting your own BUCKET-NAME and the your new User ARN

      .. code-block::

          {
              "Statement": [
                  {
                      "Sid":"PublicReadForGetBucketObjects",
                      "Effect":"Allow",
                      "Principal": {
                          "AWS": "*"
                          },
                      "Action":["s3:GetObject"],
                      "Resource":["arn:aws:s3:::BUCKET-NAME/*"
                          ]
                  },
                  {
                      "Action": "s3:*",
                      "Effect": "Allow",
                      "Resource": [
                          "arn:aws:s3:::BUCKET-NAME",
                          "arn:aws:s3:::BUCKET-NAME/*"
                      ],
                      "Principal": {
                          "AWS": [
                              "USER-ARN"
                          ]
                      }
                  }
              ]
          }

    4. Also, make sure that the CORS configuration (click "Add CORS Configuration") looks like this

        .. code-block::

            <CORSConfiguration>
                <CORSRule>
                    <AllowedOrigin>*</AllowedOrigin>
                    <AllowedMethod>GET</AllowedMethod>
                    <MaxAgeSeconds>3000</MaxAgeSeconds>
                    <AllowedHeader>Authorization</AllowedHeader>
                </CORSRule>
            </CORSConfiguration>

3. Update the Virtual Environment

    In order to configure Arches to use your new bucket, you need to install a couple of extra Django modules in your virtual environment.  These will augment Django's flexibility in how it stores uploaded media.

    Activate your virtual environment and run this command

    .. code-block::

      (ENV) $: pip install boto3==1.26 django-storages==1.13

4. Update `settings.py`

    Finally, you need to tell your app to use these new modules, give it the necessary credentials, and tell it where to store (and find) the uploaded media.  Open the your settings.py file...

    1. Find the line that defines the settings "INSTALLED_APPS" and add 'storages' to it. It should look like this

        .. code-block::

          INSTALLED_APPS = INSTALLED_APPS + (PACKAGE_NAME, 'storages',)

    2. Next, add the following lines, replacing the AWS settings values with information from earlier steps (remember the `credentials.csv` file you downloaded?)

        .. code-block::

          STORAGES = {
              "default": {
                  "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
              },
              "staticfiles": {
                  "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
              },
          }
          AWS_STORAGE_BUCKET_NAME = 'aws_bucket_name'
          AWS_ACCESS_KEY_ID = 'aws_access_key_id'
          AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'
          S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
          MEDIA_URL = S3_URL

    3. Restart your web server.

You should be good to go! To test, create a new Information Resource in your installation and upload a file. Now go back to check out your S3 bucket through the AWS console.  Your file should show up in a new folder called files within the bucket.  If you are encountering issues, be sure to let us know on the [forum](https://groups.google.com/forum/#!forum/archesproject).