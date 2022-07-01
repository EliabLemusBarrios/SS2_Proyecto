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


CLEAN_MODEL=('delete FROM region; '
'delete from sub_region; '
'delete from fecha; '
'delete from dimension; '
'delete from periodicidad; '
'delete from pais; ')

PAISES_INFLACION_ANIO=('SELECT TOP 23 p.nombre AS \'Pais\', f.anio AS \'Año\', t.max_rec AS \'Inflación\' '
'FROM fecha f, pais p, reporte r '
'JOIN '
'('
  'SELECT DISTINCT id_fecha, MAX(inflacion) AS max_rec '
  'FROM reporte '
  'GROUP BY id_fecha '
') t ON r.id_fecha  = t.id_fecha AND r.inflacion = t.max_rec '
'WHERE p.id = r.id_pais AND f.id = t.id_fecha ORDER BY f.anio ASC ')

PAIS_MAS_PIB_ANIO=('SELECT TOP 23 p.nombre AS \'Pais\', f.anio AS \'Año\', t.max_rec AS \'PIB\''
'FROM fecha f, pais p, reporte r '
'JOIN'
'('
  'SELECT DISTINCT id_fecha, MAX(PIB) AS max_rec '
  'FROM reporte '
  'GROUP BY id_fecha '
') t ON r.id_fecha  = t.id_fecha AND r.PIB = t.max_rec '
'WHERE p.id = r.id_pais AND f.id = t.id_fecha ORDER BY f.anio ASC')

PAISES_MENOS_INFLACION_ANIO=('SELECT TOP 23 p.nombre AS \'Pais\', f.anio AS \'Año\', t.max_rec AS \'Inflación\''
'FROM fecha f, pais p, reporte r '
'JOIN '
'('
  'SELECT DISTINCT id_fecha, MIN(inflacion) AS max_rec '
  'FROM reporte '
  'GROUP BY id_fecha '
') t ON r.id_fecha  = t.id_fecha AND r.inflacion = t.max_rec '
'WHERE p.id = r.id_pais AND f.id = t.id_fecha ORDER BY f.anio ASC')

PIB_POR_PAIS_3ANIOS=('SELECT p.nombre as \'Pais\', r.PIB as \'2020\', r2.PIB as \'2019\', r3.PIB as \'2018\' '
'FROM pais p, reporte r, reporte r2, reporte r3 '
'WHERE r.id_pais = p.id AND r.id_pais = r2.id_pais AND r2.id_pais = r3.id_pais AND r.id_fecha = 22 AND r2.id_fecha = 21 AND r3.id_fecha = 20; ')

INFLACION_PAIS_3ANIO=('SELECT p.nombre as \'Pais\', r.inflacion as \'2020\', r2.inflacion as \'2019\', r3.inflacion as \'2018\' '
'FROM pais p, reporte r, reporte r2, reporte r3 '
'WHERE r.id_pais = p.id AND r.id_pais = r2.id_pais AND r2.id_pais = r3.id_pais AND r.id_fecha = 22 AND r2.id_fecha = 21 AND r3.id_fecha = 20;')

TOP10_INFLACION=('SELECT TOP 10 p.nombre as \'Pais\', AVG(r.inflacion) as Promedio_Inflacion '
'FROM reporte r, pais p '
'WHERE r.id_pais = p.id '
'GROUP BY p.nombre ORDER BY Promedio_Inflacion DESC')

TOP10_PIB=('SELECT TOP 10 p.nombre as \'Pais\', AVG(r.PIB) as Promedio_PIB '
'FROM reporte r, pais p '
'WHERE r.id_pais = p.id '
'GROUP BY p.nombre ORDER BY Promedio_PIB DESC')

TOP5_ANIOS_PIB=('SELECT TOP 5 f.anio as \'Año\', AVG(r.PIB) as Promedio_PIB '
'FROM reporte r, fecha f '
'WHERE r.id_fecha = f.id '
'GROUP BY f.anio ORDER BY Promedio_PIB DESC')

TOP5_ANIOS_INFLACION=('SELECT TOP 5 f.anio as \'Año\', AVG(r.Inflacion) as Promedio_Inflacion '
'FROM reporte r, fecha f '
'WHERE r.id_fecha = f.id '
'GROUP BY f.anio ORDER BY Promedio_Inflacion DESC')



GUATE_COVID=('select f.anio,r.PIB,r.Inflacion '
'from reporte r '
 'inner join pais p on p.id = r.id_pais '
 'inner join fecha f on r.id_fecha = f.id and f.anio in (2019,2020,2021) '
'where r.id_pais=320')

SALVADOR_BITCOIN=('select f.anio,r.PIB,r.Inflacion '
'from reporte r '
 'inner join pais p on p.id = r.id_pais '
 'inner join fecha f on r.id_fecha = f.id and f.anio in (2019,2020,2021) '
'where r.id_pais=222')

CUBA=('select f.anio,r.PIB,r.Inflacion '
'from reporte r '
 'inner join pais p on p.id = r.id_pais '
 'inner join fecha f on r.id_fecha = f.id and f.anio in (2019,2020,2021) '
'where r.id_pais=192')