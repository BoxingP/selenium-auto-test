# Selenium Auto Test

Create the Selenium automation test running environment by using the AWS Cloud Development Kit (AWS CDK).
Use the AMI built by [AWS EC2 Image Builder](https://github.com/BoxingP/aws-image-builder).

Below SQLs are to create the database and table to store the logs:

### create database

```sql
CREATE DATABASE official_site_monitor
    WITH
    OWNER = postgres
    ENCODING = 'UTF-8'
    TABLESPACE = pg_default
    TEMPLATE = template0
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    CONNECTION LIMIT = -1;
```

### create table
```sql
CREATE TABLE IF NOT EXISTS public.step (
	id serial NOT NULL,
	page varchar(25) NOT NULL,
	test varchar(50) NOT NULL,
	is_summary boolean NOT NULL,
	step varchar(50) NULL,
	log_dt timestamp(0) NULL,
	spent_time numeric NULL,
	created_dt timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
	created_by varchar(25) NOT NULL DEFAULT 'System'::character varying,
	PRIMARY KEY (id)
) WITHOUT OIDS;
```

## Reference:

1. [Selenium Page Object Model with Python](https://github.com/gunesmes/page-object-python-selenium)
2. [Test Automation Project](https://github.com/startrug/selenium-python-framework)
3. [Continuous Test-Reporting with Allure](https://dev.to/habereder/continuous-test-reporting-with-allure-1ag4)
4. [pytest-json](https://github.com/mattcl/pytest-json)
5. [Application Load Balancer](https://github.com/aws-samples/aws-cdk-examples/tree/master/python/application-load-balancer)
6. [Outline Wiki on AWS](https://github.com/wowzoo/outline_on_aws)