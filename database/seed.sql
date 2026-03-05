
CREATE DATABASE empresa_db;
\c empresa_db;

CREATE TABLE departamentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    presupuesto DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    cargo VARCHAR(100),
    salario DECIMAL(10,2),
    departamento_id INT REFERENCES departamentos(id),
    fecha_ingreso DATE,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    categoria VARCHAR(100),
    precio DECIMAL(10,2),
    stock INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    empleado_id INT REFERENCES empleados(id),
    producto_id INT REFERENCES productos(id),
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2),
    total DECIMAL(12,2),
    fecha DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- DATOS DE EJEMPLO
-- ============================================

INSERT INTO departamentos (nombre, presupuesto) VALUES
('Ventas', 500000.00),
('Tecnología', 750000.00),
('Marketing', 300000.00),
('Recursos Humanos', 200000.00),
('Finanzas', 400000.00);

INSERT INTO empleados (nombre, apellido, email, cargo, salario, departamento_id, fecha_ingreso) VALUES
('Ana', 'García', 'ana.garcia@empresa.com', 'Gerente de Ventas', 8500000, 1, '2020-03-15'),
('Carlos', 'López', 'carlos.lopez@empresa.com', 'Desarrollador Senior', 9000000, 2, '2019-07-01'),
('María', 'Martínez', 'maria.martinez@empresa.com', 'Diseñadora UX', 7000000, 3, '2021-01-20'),
('Juan', 'Rodríguez', 'juan.rodriguez@empresa.com', 'Analista de RRHH', 6000000, 4, '2022-05-10'),
('Laura', 'Pérez', 'laura.perez@empresa.com', 'Vendedora', 5000000, 1, '2021-08-15'),
('Pedro', 'Sánchez', 'pedro.sanchez@empresa.com', 'Desarrollador Junior', 5500000, 2, '2023-02-01'),
('Sofía', 'Torres', 'sofia.torres@empresa.com', 'Gerente de Marketing', 8000000, 3, '2020-11-30'),
('Diego', 'Ramírez', 'diego.ramirez@empresa.com', 'Contador', 6500000, 5, '2021-04-12'),
('Valentina', 'Cruz', 'valentina.cruz@empresa.com', 'Vendedora Senior', 6000000, 1, '2020-09-05'),
('Andrés', 'Flores', 'andres.flores@empresa.com', 'DevOps Engineer', 8500000, 2, '2022-03-20');

INSERT INTO productos (nombre, categoria, precio, stock) VALUES
('Laptop Pro 15"', 'Tecnología', 4500000, 25),
('Mouse Inalámbrico', 'Accesorios', 150000, 100),
('Monitor 4K 27"', 'Tecnología', 1800000, 15),
('Teclado Mecánico', 'Accesorios', 350000, 50),
('Silla Ergonómica', 'Mobiliario', 1200000, 20),
('Auriculares Noise Cancelling', 'Audio', 800000, 35),
('Webcam HD', 'Accesorios', 250000, 60),
('Disco SSD 1TB', 'Almacenamiento', 500000, 40),
('Tablet 10"', 'Tecnología', 1500000, 18),
('Smartphone Pro', 'Tecnología', 3200000, 30);

INSERT INTO ventas (empleado_id, producto_id, cantidad, precio_unitario, total, fecha) VALUES
(1, 1, 2, 4500000, 9000000, '2024-01-15'),
(5, 2, 10, 150000, 1500000, '2024-01-20'),
(9, 3, 1, 1800000, 1800000, '2024-02-05'),
(1, 10, 3, 3200000, 9600000, '2024-02-14'),
(5, 5, 2, 1200000, 2400000, '2024-02-28'),
(9, 6, 5, 800000, 4000000, '2024-03-10'),
(1, 1, 1, 4500000, 4500000, '2024-03-22'),
(5, 7, 8, 250000, 2000000, '2024-04-01'),
(9, 4, 4, 350000, 1400000, '2024-04-15'),
(1, 9, 2, 1500000, 3000000, '2024-05-03'),
(5, 8, 6, 500000, 3000000, '2024-05-20'),
(9, 2, 15, 150000, 2250000, '2024-06-08'),
(1, 3, 2, 1800000, 3600000, '2024-06-25'),
(5, 10, 1, 3200000, 3200000, '2024-07-12'),
(9, 1, 3, 4500000, 13500000, '2024-07-30'),
(1, 6, 4, 800000, 3200000, '2024-08-14'),
(5, 9, 2, 1500000, 3000000, '2024-08-28'),
(9, 5, 1, 1200000, 1200000, '2024-09-10'),
(1, 8, 5, 500000, 2500000, '2024-09-24'),
(5, 3, 1, 1800000, 1800000, '2024-10-08'),
(9, 7, 10, 250000, 2500000, '2024-10-22'),
(1, 4, 3, 350000, 1050000, '2024-11-05'),
(5, 1, 2, 4500000, 9000000, '2024-11-19'),
(9, 10, 2, 3200000, 6400000, '2024-12-03'),
(1, 2, 20, 150000, 3000000, '2024-12-17');