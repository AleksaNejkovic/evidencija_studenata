-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 28, 2019 at 01:35 PM
-- Server version: 5.7.24
-- PHP Version: 7.2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `evidencija_studenata`
--

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

DROP TABLE IF EXISTS `korisnici`;
CREATE TABLE IF NOT EXISTS `korisnici` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ime` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `prezime` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `lozinka` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`id`, `ime`, `prezime`, `email`, `lozinka`) VALUES
(14, 'Dusan', 'Djuric', 'dd@gmail.com', 'pbkdf2:sha256:150000$LteceTaI$f6a32ebdc8c51ee191c9bca66e4b5ab96aefe0777993e011eef2ea6230f3acd5');

-- --------------------------------------------------------

--
-- Table structure for table `ocene`
--

DROP TABLE IF EXISTS `ocene`;
CREATE TABLE IF NOT EXISTS `ocene` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `predmet_id` int(11) NOT NULL,
  `ocena` smallint(6) NOT NULL,
  `datum` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `predmeti_strani` (`predmet_id`),
  KEY `studenti_strani` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `predmeti`
--

DROP TABLE IF EXISTS `predmeti`;
CREATE TABLE IF NOT EXISTS `predmeti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sifra` varchar(30) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `naziv` varchar(30) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `godina_studija` smallint(6) NOT NULL,
  `ESPB` int(11) NOT NULL,
  `obavezni_izborni` varchar(10) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `predmeti`
--

INSERT INTO `predmeti` (`id`, `sifra`, `naziv`, `godina_studija`, `ESPB`, `obavezni_izborni`) VALUES
(1, '1234', 'Matematika', 1, 6, 'Obavezni');

-- --------------------------------------------------------

--
-- Table structure for table `studenti`
--

DROP TABLE IF EXISTS `studenti`;
CREATE TABLE IF NOT EXISTS `studenti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ime` varchar(100) COLLATE utf8_bin NOT NULL,
  `ime_roditelja` varchar(100) COLLATE utf8_bin NOT NULL,
  `prezime` varchar(100) COLLATE utf8_bin NOT NULL,
  `broj_indexa` varchar(10) COLLATE utf8_bin NOT NULL,
  `godina_studija` smallint(6) NOT NULL,
  `JMBG` bigint(20) NOT NULL,
  `datum_rodjenja` date NOT NULL,
  `ESPB` int(11) DEFAULT NULL,
  `prosek_ocena` float DEFAULT NULL,
  `broj_telefona` varchar(20) COLLATE utf8_bin NOT NULL,
  `email` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `studenti`
--

INSERT INTO `studenti` (`id`, `ime`, `ime_roditelja`, `prezime`, `broj_indexa`, `godina_studija`, `JMBG`, `datum_rodjenja`, `ESPB`, `prosek_ocena`, `broj_telefona`, `email`) VALUES
(5, 'Aleksa', 'Olivera', 'Nejković', 'PEp8/17', 3, 1231232131231, '1998-06-27', NULL, NULL, '1023012301', 'aleksa.nejkovic@vtsnis.rs');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ocene`
--
ALTER TABLE `ocene`
  ADD CONSTRAINT `predmeti_strani` FOREIGN KEY (`predmet_id`) REFERENCES `predmeti` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `studenti_strani` FOREIGN KEY (`student_id`) REFERENCES `studenti` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
