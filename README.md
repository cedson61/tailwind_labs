# tailwind_labs
This repo includes the code powering [tailwind labs](http://labs.tailwindsolutions.com) - my demo site. It is arranged
into a set of (theoretically) reusable django apps.

## Items
* A simple example of using django's class-based generic views to create, read, update and delete
"items" from a [PostgreSQL](http://www.postgresql.org/) database, all managed through Django's ORM
* Implemented "soft delete" by overriding views' default behaviors (items are never deleted from the db,
just deactivated)
* Authentication is required for all Items views, courtesy of braces' LoginRequiredMixin
* Automated Tests! Finally delved into Django's testing and wrote comprehensive tests.

## Smart Sort
* Demonstrates a simple API for remotely sorting complex data values
* AJAX is used to send the data to and from the API
* The API uses regular Expression pattern matching and custom sort rules

## CSV Analyzer
* Demonstrates use of [pandas](http://pandas.pydata.org/) to read and analyze the contents of a csv file.
