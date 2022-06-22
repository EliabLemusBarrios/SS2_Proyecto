DROP_TABLES=('DROP TABLE IF EXISTS temporal;'
'DROP TABLE IF EXISTS temporal_inflacion;'
'DROP TABLE IF EXISTS temporalISO3166;'
'DROP TABLE IF EXISTS reporte;'
'DROP TABLE IF EXISTS pais;'
'DROP TABLE IF EXISTS dimension;'
'DROP TABLE IF EXISTS fecha;'
'DROP TABLE IF EXISTS region;'
'DROP TABLE IF EXISTS periodicidad;'
'DROP TABLE IF EXISTS sub_region;')

TEMPORAL_CREATION=(
    'CREATE TABLE temporalISO3166('
    'country_name varchar(250), '
    'alpha3 varchar(10), '
    'country_code BIGINT, '
    'region varchar(250), '
    'region_code BIGINT, '
    'sub_region varchar(250),'
    'sub_region_code BIGINT ); '
    'CREATE TABLE temporal('
    'series_name varchar(250), '
    'country_name varchar(250), '
    'country_code varchar(20), '
    '"1990" FLOAT, '
    '"2000" FLOAT, '
    '"2001" FLOAT, '
    '"2002" FLOAT, '
    '"2003" FLOAT, '
    '"2004" FLOAT, '
    '"2005" FLOAT, '
    '"2006" FLOAT, '
    '"2007" FLOAT, '
    '"2008" FLOAT, '
    '"2009" FLOAT, '
    '"2010" FLOAT, '
    '"2011" FLOAT, '
    '"2012" FLOAT, '
    '"2013" FLOAT, '
    '"2014" FLOAT, '
    '"2015" FLOAT, '
    '"2016" FLOAT, '
    '"2017" FLOAT, '
    '"2018" FLOAT, '
    '"2019" FLOAT, '
    '"2020" FLOAT, '
    '"2021" FLOAT);'
    'CREATE TABLE temporal_inflacion('
    'series_name varchar(250), '
    'country_name varchar(250), '
    'country_code varchar(20), '
    '"1990" FLOAT, '
    '"2000" FLOAT, '
    '"2001" FLOAT, '
    '"2002" FLOAT, '
    '"2003" FLOAT, '
    '"2004" FLOAT, '
    '"2005" FLOAT, '
    '"2006" FLOAT, '
    '"2007" FLOAT, '
    '"2008" FLOAT, '
    '"2009" FLOAT, '
    '"2010" FLOAT, '
    '"2011" FLOAT, '
    '"2012" FLOAT, '
    '"2013" FLOAT, '
    '"2014" FLOAT, '
    '"2015" FLOAT, '
    '"2016" FLOAT, '
    '"2017" FLOAT, '
    '"2018" FLOAT, '
    '"2019" FLOAT, '
    '"2020" FLOAT, '
    '"2021" FLOAT);')

CREATE_MODEL=(
    'CREATE TABLE dimension ('
    '[id] INT NOT NULL IDENTITY(1,1) PRIMARY KEY, '
    '[descripcion] VARCHAR(200) NOT NULL '
    ') ;'
    'CREATE TABLE fecha ('
    '[id] INT NOT NULL IDENTITY(1,1) PRIMARY KEY, '
    '[anio] int NOT NULL '
    ') ;'
    'CREATE TABLE region ('
    '[id] INT NOT NULL PRIMARY KEY, '
    '[nombre] VARCHAR(250) NOT NULL '
    ') ;'
    'CREATE TABLE periodicidad ( '
    '[id] INT NOT NULL IDENTITY(1,1) PRIMARY KEY, '
    '[descripcion] varchar(250) NOT NULL '
    ') ;'
    'CREATE TABLE sub_region ( '
    '[id] INT NOT NULL PRIMARY KEY, '
    '[nombre] varchar(250) NOT NULL '
    ') ;'
    'CREATE TABLE pais ( '
    ' [id] INT NOT NULL PRIMARY KEY,'
    ' [id_region] INT FOREIGN KEY REFERENCES region(id),'
    ' [id_sub_region] INT FOREIGN KEY REFERENCES sub_region(id),'
    ' [nombre] VARCHAR(200) NOT NULL '
    ') ;'
    'CREATE TABLE reporte ( '
    '[id] INT NOT NULL IDENTITY(1,1) PRIMARY KEY,'
    '[inflacion] FLOAT NOT NULL,'
    '[PIB] FLOAT NOT NULL,'
    '[id_pais] INT FOREIGN KEY REFERENCES pais(id),'
    '[id_periodicidad] INT FOREIGN KEY REFERENCES periodicidad(id),'
    '[id_dimension] INT FOREIGN KEY REFERENCES dimension(id),'
    '[id_fecha] INT FOREIGN KEY REFERENCES fecha(id),'
    ') ;'
)
FILL_MODEL=(
    'INSERT INTO region(id, nombre)'
    'SELECT DISTINCT region_code, region  FROM temporalISO3166 WHERE region_code != 0 ORDER BY region  ASC;'
    'INSERT INTO sub_region (id, nombre)'
    'SELECT DISTINCT sub_region_code, sub_region  FROM temporalISO3166 WHERE region_code != 0 ORDER BY sub_region  ASC ;'
    'INSERT INTO fecha (anio)'
    'SELECT COLUMN_NAME'
    'FROM INFORMATION_SCHEMA.COLUMNS'
    'WHERE TABLE_NAME = N\'temporal_inflacion\' AND ISNUMERIC(COLUMN_NAME) = 1 ORDER BY COLUMN_NAME ASC;'
    'INSERT INTO dimension (descripcion) VALUES (\'Porcentaje\');'
    'INSERT INTO periodicidad (descripcion) VALUES (\'Anual\');'
    'INSERT INTO pais'
        'SELECT DISTINCT ti.country_code, r.id, sr.id, ti.country_name FROM temporalISO3166 ti, region r, sub_region sr '
        'WHERE ti.region_code = r.id AND sr.id = ti.sub_region_code ORDER BY ti.country_name ASC;'    
)   
REGION=('INSERT INTO region(id, nombre)'
'SELECT DISTINCT region_code, region  FROM temporalISO3166 WHERE region_code != 0 ORDER BY region  ASC;')

SUB_REGION=('INSERT INTO sub_region (id, nombre)'
'SELECT DISTINCT sub_region_code, sub_region  FROM temporalISO3166 WHERE region_code != 0 ORDER BY sub_region  ASC ;')

FECHA=('INSERT INTO fecha (anio) '
'SELECT COLUMN_NAME '
'FROM INFORMATION_SCHEMA.COLUMNS '
'WHERE TABLE_NAME = \'temporal_inflacion\' AND ISNUMERIC(COLUMN_NAME) = 1 ORDER BY COLUMN_NAME ASC; ')

DIMENSION=('INSERT INTO dimension (descripcion) VALUES (\'Porcentaje\');')

PERIODICIDAD=('INSERT INTO periodicidad (descripcion) VALUES (\'Anual\');')
PAIS=('INSERT INTO pais '
'SELECT DISTINCT ti.country_code, r.id, sr.id, ti.country_name FROM temporalISO3166 ti, region r, sub_region sr '
'WHERE ti.region_code = r.id AND sr.id = ti.sub_region_code ORDER BY ti.country_name ASC; ')


