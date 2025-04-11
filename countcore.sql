-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Tempo de geração: 24/03/2025 às 20:17
-- Versão do servidor: 9.1.0
-- Versão do PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `countcore`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `tabelaadm`
--

DROP TABLE IF EXISTS `tabelaadm`;
CREATE TABLE IF NOT EXISTS `tabelaadm` (
  `id_adm` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  `senha` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_adm`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tabelaadm`
--

INSERT INTO `tabelaadm` (`id_adm`, `nome`, `senha`) VALUES
(1, 'Rafael', '123123'),
(2, 'Samir', 'Cachorro123123');

-- --------------------------------------------------------

--
-- Estrutura para tabela `tabela foto`
--

DROP TABLE IF EXISTS `tabela foto`;
CREATE TABLE IF NOT EXISTS `tabela foto` (
  `id_foto` int NOT NULL AUTO_INCREMENT,
  `link_foto` varchar(1000) COLLATE utf8mb4_general_ci NOT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id_foto`),
  KEY `pk_usuario2` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tabela placa`
--

DROP TABLE IF EXISTS `tabela placa`;
CREATE TABLE IF NOT EXISTS `tabela placa` (
  `id_placa` int NOT NULL AUTO_INCREMENT,
  `placa` varchar(7) COLLATE utf8mb4_general_ci NOT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id_placa`),
  KEY `pk_usuario` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tabela usuario`
--

DROP TABLE IF EXISTS `tabela usuario`;
CREATE TABLE IF NOT EXISTS `tabela usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  `placa_id` int NOT NULL,
  `foto_id` int NOT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `pk_placa` (`placa_id`),
  KEY `pk_foto` (`foto_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `tabela foto`
--
ALTER TABLE `tabela foto`
  ADD CONSTRAINT `pk_usuario2` FOREIGN KEY (`usuario_id`) REFERENCES `tabela usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- Restrições para tabelas `tabela placa`
--
ALTER TABLE `tabela placa`
  ADD CONSTRAINT `pk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `tabela usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- Restrições para tabelas `tabela usuario`
--
ALTER TABLE `tabela usuario`
  ADD CONSTRAINT `pk_foto` FOREIGN KEY (`foto_id`) REFERENCES `tabela foto` (`id_foto`) ON DELETE CASCADE ON UPDATE RESTRICT,
  ADD CONSTRAINT `pk_placa` FOREIGN KEY (`placa_id`) REFERENCES `tabela placa` (`id_placa`) ON DELETE CASCADE ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
