# Django FullStack Project

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


# Tech used

## Back-end

- [Python 3.8](https://docs.python.org/3.8/whatsnew/3.8.html)
- [Django 3.1](https://docs.djangoproject.com/en/3.1/)
- [AWS S3](https://aws.amazon.com/s3/)
    - To host static and media files.
- [Stripe](www.stripe.com)
    - To secure payment process.  

## Front-end

- Styling is written in [SCSS](https://sass-lang.com).
- [Bootstrap4](https://getbootstrap.com/) to set up our basic template layout.
- [jQuery](https://jquery.com/) library is used for DOM manipulation and is required for Bootstrap.

## Other tech
- [Selenium](https://www.selenium.dev/documentation/en/)
	I use Selenium to conduct End-to-End tests with Firefox and Chrome.  


# Contributing


1. You first need to fork the repo
2. Set the Virtual Environment with python3.8
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
6. Run the app  
    ```bash  
    python manage.py runserver
    ```
7. Watch your SCSS files  
    I use [NPM](https://www.npmjs.com/) and run the following command in a separate terminal to watch scss files changes and 
    compress into css:  
    ```bash
    npm run sass
    ```

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
