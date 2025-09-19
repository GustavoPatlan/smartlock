-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: smartlock
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `casilleros`
--

DROP TABLE IF EXISTS `casilleros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `casilleros` (
  `IDE` varchar(200) NOT NULL,
  `LOCKER` varchar(20) DEFAULT 'SIN ASIGNAR',
  `CNOMBRE` varchar(50) DEFAULT 'SIN ASIGNAR',
  `ZONA` varchar(100) DEFAULT 'SIN ASIGNAR',
  `CIUDAD` varchar(100) DEFAULT 'SIN ASIGNAR',
  `ESTADO` varchar(100) DEFAULT 'SIN ASIGNAR',
  `DISPONIBILIDAD` varchar(50) DEFAULT 'LIBRE',
  PRIMARY KEY (`IDE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registros`
--

DROP TABLE IF EXISTS `registros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registros` (
  `IDE` int NOT NULL AUTO_INCREMENT,
  `CORREO` varchar(100) DEFAULT NULL,
  `HORA` time DEFAULT NULL,
  `FECHA` date DEFAULT NULL,
  `ESPACIO` varchar(20) DEFAULT NULL,
  `CASILLERO` varchar(50) DEFAULT NULL,
  `UBICACION` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`IDE`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `CORREO` varchar(100) NOT NULL,
  `NOMBRES` varchar(100) DEFAULT NULL,
  `APELLIDOS` varchar(100) DEFAULT NULL,
  `LLAVE` varchar(50) DEFAULT NULL,
  `LOCKER` varchar(20) DEFAULT 'SIN ASIGNAR',
  `CODIGO` varchar(20) DEFAULT 'SIN ASIGNAR',
  `CNOMBRE` varchar(50) DEFAULT 'SIN ASIGNAR',
  `ZONA` varchar(100) DEFAULT 'SIN ASIGNAR',
  `CIUDAD` varchar(100) DEFAULT 'SIN ASIGNAR',
  `ESTADO` varchar(100) DEFAULT 'SIN ASIGNAR',
  PRIMARY KEY (`CORREO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-23 10:39:00
