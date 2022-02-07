PROVINCIAS = (  (1, 'Buenos Aires'), (2, 'Córdoba'), (3, 'Santa Fe'),
                (4, 'Tucumán'), (5, 'Misiones'), (6, 'Corrientes'),
                (7, 'Entre Ríos'), (8, 'Formosa'), (9, 'Chaco'),
                (10, 'San Luís'), (11, 'San Juan'), (12, 'Mendoza'),
                (13, 'Salta'), (14, 'Jujuy'), (15, 'Catamarca'),
                (16, 'La Rioja'), (17, 'La Pampa'), (18, 'Tierra Del Fuego'),
                (19, 'Rio Negro'), (20, 'Chubut'), (21, 'Neuquén'),
                (22, 'Santa Cruz'), (23, 'Santiago Del Estero'), (24, 'CABA')   )

SEXO = (    (1, 'Femenino'), (2, 'Masculino')   )

ESTADO_CIVIL = (    (1, 'Soltero'), (2, 'Casado/concubino'), (3, 'Separado/divorciado'), (4, 'Viudo')   )

AREA = (    (1, 'Urbana'), (2, 'Rural') )

ETNIA = (   (1, 'Caucásico'), (2, 'Mestizo'), (3, 'Asiático'), (4, 'Afroamericano'), (5, 'Desconocido')   )

CUMPLE_CRITERIO = ( ('1', 'Sí'), ('0', 'No')    )

SUBTIPO = ( (1, 'Pura'), (2, 'Juvenil'), (3, 'Asociada a Artritis Psoriásica'),
            (4, 'Asociada a enfermedad Inflamatoria Intestinal (EII)'), (5, 'Artritis Reactiva')    )

TIPO = (    ('1', 'No radiográfica'), ('2', 'Radiográfica') )

CRITERIO_POS_NEG = ( ('1', 'Positivo'), ('0', 'Negativo')    )

CRITERIO_POS_NEG_BLANK = ( (2, 'No aplica'), (1, 'Positivo'), (0, 'Negativo')    )

RESULT_RADIOGRAFIA = (  ('1', 'Grado 0 uni/bilateral'), ('2', 'Grado 1 uni/bilateral'),
                        ('3', 'Grado 2 unilateral'), ('4', 'Grado 2 bilateral'),
                        ('5', 'Grado 3 unilateral'), ('6', 'Grado 3 bilateral'),
                        ('7','Grado 4 unilateral'), ('8', 'Grado 4 bilateral'), ('9', 'No se hizo')     )

ESTUD_Y_RESULT = ( ('1', 'Sí y fue positivo'), ('2', 'Sí y fue negativo'), ('3', 'No se hizo') )