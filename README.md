# Django FullStack Project

[***Shapers is live here***](https://test-shapers.herokuapp.com/)

*Shapers sends emails to users. Don't spam innocent people and provide yours ;)*

Table Of Contents

- [Overview](#overview)
- [Design](#design)
    - [UX](#ux)
        - [Personas & user stories](#personas--users-stories)
        - [Information Architecture](#information-architecture)
        - [Wireframes](#wireframes)
    - [Database](#database)
- [Workflow](#workflow)
    - [Story Map](#story-map)
- [Tech used](#tech-used)
- [Contributing](#contributing)
    - [Testing](#testing)
        - [Unit tests](#unit-tests)
        - [End-To-End](#end-to-end-tests)
        - [Stripe Webhooks](#stripe-webhooks)


# Overview

This E-commerce project allows users to purchase 3D printed design products (miniatures, gadgets, small home and office 
accessories, etc.).
While the 3D printing service is clearly out of this project's scope, it handles all the functionality of an e-commerce app: 
browsing through design products and categories, users authentication, payment and users customized interaction with the platform.

The platform has two main types of users:
- Customers, purchasing design products in the store.  
- Partners, selling their designs and purchasing any products in the store.  

Customers have the possibility to choose the material and color for each product they purchase. They can keep track of 
their orders, rate and comment after payment and subscribe for email alerts for delivery status.  
Partners can, additionally, upload their designs and choose materials and colors that will be available to the customers. 
They may edit these choices, upload a new design version or remove it from the store. They can subscribe for email alerts when a product 
is sold, when a customer rates or comments one of their designs.  


# Design

## UX

All UX preliminary work can be found in [ux_documentation](./ux_documentation).

### Personas & Users stories

[Personas and user stories](./ux_documentation/persona_user_stories.md) are detailed in a separate file in the ux documentation 
directory.

### Information Architecture

The very first step prior to working on any wireframe is to set the [zoning](./ux_documentation/zoning.jpg).

- All user centric features are accessible from the user icon in navbar once logged in. The navbar displays all 
session related infos (cart, etc.).  
- All app core features (browsing, product categories, blog, etc.) are accessible from the side menu.  
- All legal information and platform support is located in the footer.  

Such compartmentalization improves the first-time learning experience and prevents 
neither menus to become overloaded with links and information.  

A sub-nav zone as a navigation feedback may be added to compensate mobile visibility on nested subtree 
categories. This can become critical with bad network throttling or on a slow device. While this is less necessary on larger 
screens I've decided I would keep it for visual consistency (for now).  

The content area is divided in two zones, main content and a search field present in all browsing pages so the users can 
adjust their keyword search with fewer interactions.  


### Wireframes

I've designed the wireframes in an iterative process going through all user stories based on their priority. This approach 
helps creating an efficient features and information architecture by adding the bare minimum and making any necessary 
adjustments in respect of different users needs.  
The [user stories wireframes](./ux_documentation/user_stories_wireframes.pdf) shows the results on the persona 'priority device'
 (device the user is more likely to connect with).


## Database

Here is a draft of the [Database Relationship Diagram](./ux_documentation/shapers_db_design.png).


# Workflow

## Story Map

I have grouped user stories in this [Story Map](./ux_documentation/shapers_storymap.pdf) following the MoSCoW method
before creating the backlog and organizing sprints in [ORA](https://ora.pm/) using Agile Estimation technique.  

With Tom being the main persona grouping all core features, I’ve planned a "pre-release" version (actual true 
MVP: sprint3).  
This pre-release version may not last long against competitors but the concept of pre-release is to hold stake-holder’s breath 
a bit longer (as well as customers in case of pre-launch marketing campaign) should the development be severely delayed.  

### When things go wrong

As some things got in the way and out of hand, this project suffers the consequences in terms of delay, and features delivered. 
The original planning helped me stay on track. With the help of my mentor Aaron, we were able to re-prioritize realistically 
the most expected and valuable features before this project's submission deadline (release date).  
I will definitively finish it later.


## Git add, stash, commit, apply, repeat !
When working on a feature or implementation I usually save it in the staging area but then start to work on the next 
implementation instead of committing files. I would then stash the next step code blocks/lines to test (manual or automated) 
the current implementation before committing these changes. Retrieve the code blocks from the stash work on it more ( if need be) and repeat ! 
This helps breaking large commits into smaller ones with a cleaner commit tree for another developer to pickup .
I’m using Gitkraken that makes this process easier.


[To top](#django-fullstack-project)

# Tech used

## Back-end

- [Python 3.8](https://docs.python.org/3.8/whatsnew/3.8.html)
- [Django 3.1](https://docs.djangoproject.com/en/3.1/)
- [AWS S3](https://aws.amazon.com/s3/)
    - To host static and media files.
- [Stripe](https://www.stripe.com)
    - To secure payment process.  

## Front-end

- Styling is written in [SCSS](https://sass-lang.com).
- [Bootstrap4](https://getbootstrap.com/) to set up our basic template layout.
- [jQuery](https://jquery.com/) library is used for DOM manipulation and is required for Bootstrap.
- [<model-viewer>](https://modelviewer.dev/) from Google.  
    As dealing with 3D printing files, it is essential to have an interactive tool to display 
    the 3D model in the browser.

## Other tech
- [Selenium](https://www.selenium.dev/documentation/en/)
	I use Selenium to conduct End-to-End tests with Firefox and Chrome.  

## Softwares
- [PyCharm](https://www.jetbrains.com/pycharm/)  
    My favorite IDE of all !!!
- [GitKraken](https://www.gitkraken.com/)  
    Handy to visualize the commit tree, stashes, diff split view etc. It is an essential tool in my workflow along with PyCharm VCS.
- [Ora](https://ora.pm/)  
    Project management. Initially for planning the workload, prioritizing tasks and monitoring (for velocity and check my burndown charts ;).
    Unfortunately with few things getting in the middle and a tight deadline, I've left that aside focusing on development rather than the tools.
- [Draw.io](https://www.diagrams.net/)  
    For the Database design.
- [Maya](https://www.autodesk.com/products/maya/) & [Blender](https://www.blender.org/)  
    For dealing with glb & gltf files required by google's <model-viewer>.
    I've been using Maya for over 15years and decided to give Blender a try.

## Extra Libraries
- [Fontawesome](https://fontawesome.com/)  
    Used for few icons. Its rounded design (free version) does not fit much in here.
- [Google Font](https://fonts.google.com/)
    Using Google fonts relying on CDN.

[To top](#django-fullstack-project)

# Contributing

## Requirements

You will need to create an account for each of the following:  
- Stripe
- Gmail, or another (unless you use the Django emailBackend)
- AWS S3 (for deployment, see `heroku` git branch)

## Running the project locally

1. You first need to fork the repo
2. Set the Virtual Environment with python3.8
    ```bash
    virtualenv venv --python=python3.8
    ```
   *Should you need to install it, a handy procedure on
    [Tecadmin.net](https://tecadmin.net/install-python-3-8-ubuntu/).*
3. Install the project’s dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations
    ```bash
    python manage.py migrate
    ```
5. Populate database with fixtures to start app with minimum data content (I'll add these soon).
    ```bash
    python manage.py loaddata categories.json products.json
    ```
6. Create your django admin super user
    ```bash
   python manage.py createsuperuser
    ```
   *Remember that users log in the app with email address only.  
   Don't forget to provide your real one to receive the confirmation emails.*
7. Set your Environment Variables or use local files.  
    - For emails, set in a gitignored file (`mail_config`):
        - EMAIL_HOST_USER
        - EMAIL_HOST_PASSWORD
        - DEFAULT_FROM_EMAIL
    - STRIPE requires your
        - STRIPE_PUBLIC_KEY
        - STRIPE_SECRET_KEY
        - STRIPE_WEBHOOK_SECRET_KEY
8. Run the app  
    ```bash  
    python manage.py runserver
    ```
9. Watch SCSS files changes  
    I use [NPM](https://www.npmjs.com/) and run the following command in a separate terminal to 
    watch scss file changes and compress css into their original app:  
    ```bash
    npm run sass
    ```

## Deployment

[Shapers](https://test-shapers.herokuapp.com/) is deployed on [Heroku](https://www.heroku.com/).

**I use a dedicated branch for Heroku deployment, simply called `heroku`.
There lies the settings for AWS S3 and other specific requirements for Heroku to build the app.**

### Procedure :

*Install Heroku toolbelt if you want to use the CLI*

*Remember to update the requirements.txt if you add/remove any dependencies. 
`pip freeze --local > requirements.txt`.*

When the new release is ready :
1. Change to `heroku` branch: `git checkout heroku`.
2. Create the app on Heroku (via dashboard)
    - Add/Update the `ALLOWED_HOSTS` in the root project `settings.py`:  
    `<heroku_app_name>.herokuapp.com`
    - Add the associated git repo and check your remote repositories:  
        ```bash
        git remote add heroku https://git.heroku..com/<heroku_app_name>.git
        git remote -v
        ``` 
3. Create your database on Heroku (CLI):  
    ```bash
   heroku addons:create --app=<heroku_app_name> heroku-postgresql:hobby-dev
    ```
4. Install Heroku deployment dependencies (different requirements.txt on `heroku` branch):  
    ```bash
    pip install -r requirements.txt
   ```  
    or install them as follow:
    ```bash
   pip install gunicorn psycopg2-binary dj_database_url
    ```
5. Create your Procfile for Gunicorn to run the app on Heroku server: 
    ```bash
    echo web: gunicorn <django_project_name>.wsgi:application > Procfile
   ```
6. Set Heroku Config Variables
    - SECRET_KEY
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_STORAGE_BUCKET_NAME
    - EMAIL_FROM_DEFAULT
    - EMAIL_HOST_PASSWORD
    - EMAIL_HOST_USER
    - STRIPE_PUBLIC_KEY
    - STRIPE_SECRET_KEY
    - STRIPE_WEBHOOK_SECRET_KEY
    - DISABLE_COLLECTSTATIC = 1
7. Now to create and populate our deployed database on Heroku:
    1. Temporally copy the `DATABASE_URL` string from Heroku config vars into the settings.py as follow:  
    ```bash
    DATABASES = {
        'default': dj_database_url.parse(‘<database_url_string>’)
    }
    ```
   2. Now we're ready :
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # remember to provide your real email
   python loaddata categories.json products.json
   ```
   3. Now revert the DATABASE setting to its previous state.
8. You may choose to collect static files when pushing to Heroku or do it your self by disabling collect static :  
    `heroku config:set DISABLE_COLLECTISTATIC=1`  
    or upload the media and static files on AWS S3 independently :  
    `python manage.py collectstatic`  
    or using AWS website by dropping the directories into your bucket.
9.  Finally ready to push on to Heroku:
    ```bash
    git push heroku heroku:master
    ```

The app is now running live !

[To top](#django-fullstack-project)

## Testing

I love automated tests. They really ease and speed up the development process when the project grows considerably. It ensures no feature is broken with each new addition.
Unfortunately being short on time I couldn't keep implementing new features nor updating with the appropriate tests or modifying them.
Last implementation with its batch of tests : 
https://github.com/exipso/shapers/commit/1804d40b0f1b50b8da7e1b053152d58c0a52f4a9
At that point all tests passed with a coverage of 100% meaning the app was stable.

I’ve separated unit and e2e testing to speed up the process. 

### Unit tests

Using coverage as follow:
```bash
coverage run --source=<app>[,<app>]  manage.py test <app>.tests.unit [<app>.tests.unit]
coverage report && coverage html
```

### End-To-End tests

End to End tests are conducted with Firefox 78 and Chrome 84.  
You need Selenium installed and the appropriate webdrivers according to the browser’s version 
you’ll be running these tests with.  
Gecko drivers for Firefox :  
https://github.com/mozilla/geckodriver/releases  
Google Chrome :  
https://sites.google.com/a/chromium.org/chromedriver/downloads

Check installation of webdrivers according to your os:
`usr/local/bin/`

Run the tests :  
```bash
coverage run –-source=<app>  manage.py test <app>.tests.e2e
coverage report && coverage html
```

To specify one of the browsers to run these tests (as they should contain same 
tests but with dedicated browser) :
```bash
coverage run –-source=<app>  manage.py test <app>.tests.e2e.test_<app>_ff
```

### Stripe Webhooks

Once you forked the repo, you can test the webhook endpoints through your Stripe account dashboard. It sends 
generic webhooks without any specific data required by the app. So I decided to give the Stripe CLI a shot.
Documentation [here](https://stripe.com/docs/stripe-cli). 

1. Follow Stripe Cli installation steps depending on your os
2. Run command to listen for webhooks
    ```bash
    ./stripe listen --forward-to 127.0.0.1:8000/checkout/webhooks/
    ```
3. In a separate terminal trigger events and check your IDE terminal (you might want to temporally add print statements)
    ```bash
    ./stripe trigger payment_intent.succeeded
    ```
   
_You'll want to comment out the form submission in `checkout.js` to extend testing its behaviour._
 
#### Using Fixtures
 
To test the webhook write the fixtures according to the webhook type you want to test.  
[My payment succeeded fixture](stripe_fixtures.json).  
Then, while listening as before simply run in a separate terminal:
```bash
./stripe fixtures ./stripe_fixtures.json
```
The `username` in the fixture metadata should be a user in the database (yours as superuser).  
And the `cart_content` should be matching the dictionary used in the cart and checkout process: `{'product_id': quantity}`.  
Being short on time, I could not get the billing details into the fixtures properly to test the `payment_intent.succeeded`.
A quick workaround was to duplicate and comment out the order creation block:
1. Passing string directly into the required fields :
    ```bash
    order_process = Order.objects.create(
                        full_name="John Soe",
                        user_profile=user_profile,)
    ```
2. To create order line products, as the fixture passes in the metadata as string:
    ```bash
    cart_content = eval(cart_content)
    ```
   
[To top](#django-fullstack-project)

## Code

- [<model-viewer>](https://modelviewer.dev/)  
    The 3d printing files interaction in products gallery relies on Google's model-viewer.

- [Bootstrap](https://getbootstrap.com/docs/4.4/getting-started/introduction/)  
    Using extensively the Grid System and overriding or fine tuning them when necessary.  

## Credits

### Media

- [Poly](https://poly.google.com/)  
    Since I did not have the time to add my own 3D models I used Google's Poly materials under BY CC license.

### Content

- All the content (app and Readme) was written by [myself](https://github.com/exipso).

### Acknowledgement

- My mentor [Aaron Sinnott](https://github.com/aaronsnig501), for his encouraging support, helping me manage this project 
and his precious insights.
