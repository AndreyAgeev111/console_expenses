## A console application about your expenses or income
This is the basic version of the application, is under development. 
Here the Postgresql database was used, the code for creating tables for storing data:
### Table expenses
```SQL

    CREATE TABLE IF NOT EXISTS public.expenses
    (
        id integer NOT NULL DEFAULT nextval('expenses_id_seq'::regclass),
        price double precision NOT NULL,
        comment text COLLATE pg_catalog."default",
        date_of_day date NOT NULL DEFAULT '2001-07-23'::date,
        id_section integer,
        CONSTRAINT expenses_pkey PRIMARY KEY (id),
        CONSTRAINT fk_id_section FOREIGN KEY (id_section)
            REFERENCES public.sections (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,
        CONSTRAINT price CHECK (price > 0::double precision) NOT VALID
    )
    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.expenses
        OWNER to postgres;
```
### Table sections
```SQL

    CREATE TABLE IF NOT EXISTS public.sections
    (
        id integer NOT NULL DEFAULT nextval('sections_id_seq'::regclass),
        section text COLLATE pg_catalog."default" NOT NULL,
        CONSTRAINT sections_pkey PRIMARY KEY (id),
        CONSTRAINT sections_section_key UNIQUE (section)
    )

    TABLESPACE pg_default;
    
    ALTER TABLE IF EXISTS public.sections
        OWNER to postgres;
```
The user manual is also provided:
![Alt-текст](https://github.com/AndreyAgeev111/console_expenses/blob/master/res/manual.png "Manual")
There are different types of visual representation of data:
![Alt-текст](https://github.com/AndreyAgeev111/console_expenses/blob/master/res/bar.png "Bar")
![Alt-текст](https://github.com/AndreyAgeev111/console_expenses/blob/master/res/pie.png "Pie")

### Example of how the program works
![Alt-текст](https://github.com/AndreyAgeev111/console_expenses/blob/master/res/example_1.png "Example")
![Alt-текст](https://github.com/AndreyAgeev111/console_expenses/blob/master/res/example_2.png "Example")
