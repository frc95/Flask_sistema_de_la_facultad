instructions = [
    'DROP TABLE IF EXISTS alu_mat;',
    'DROP TABLE IF EXISTS materia;',
    'DROP TABLE IF EXISTS usuario;',
    """
        CREATE TABLE usuario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            type TEXT NOT NULL
        );
    """,
    
    """
        CREATE TABLE materia (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre TEXT NOT NULL,
            cuatrimestre TEXT NOT NULL,
            cupo INT NOT NULL,
            anio INT NOT NULL,
            turno TEXT NOT NULL,
            id_profesor INT NOT NULL,
            FOREIGN KEY (id_profesor) REFERENCES usuario (id)
        );
    """,
    
    """
        CREATE TABLE alu_mat (
            id_alu INT NOT NULL,
            id_mat INT NOT NULL,
            nota_uno INT NOT NULL,
            nota_dos INT NOT NULL,
            promedio FLOAT NOT NULL,
            PRIMARY KEY (id_alu, id_mat),
            FOREIGN KEY (id_alu) REFERENCES usuario (id),
            FOREIGN KEY (id_mat) REFERENCES materia (id)
        );
    """
]