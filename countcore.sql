-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 15/04/2025 às 04:57
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

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

CREATE TABLE `tabelaadm` (
  `id_adm` int(11) NOT NULL,
  `nome` varchar(80) NOT NULL,
  `senha` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tabelaadm`
--

INSERT INTO `tabelaadm` (`id_adm`, `nome`, `senha`) VALUES
(1, 'Rafael', '123123'),
(2, 'Samir', 'Cachorro123123');

-- --------------------------------------------------------

--
-- Estrutura para tabela `tabelafoto`
--

CREATE TABLE `tabelafoto` (
  `id_foto` int(11) NOT NULL,
  `link_foto` varchar(1000) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tabelafoto`
--

INSERT INTO `tabelafoto` (`id_foto`, `link_foto`, `usuario_id`) VALUES
(1, 'LINK', 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `tabelahistorico`
--

CREATE TABLE `tabelahistorico` (
  `id_historico` int(11) NOT NULL,
  `placa_id` int(11) NOT NULL,
  `data` date NOT NULL,
  `hora` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tabelahistorico`
--

INSERT INTO `tabelahistorico` (`id_historico`, `placa_id`, `data`, `hora`) VALUES
(1, 1, '2025-04-14', '00:00:00'),
(2, 1, '2025-04-14', '23:13:45'),
(3, 1, '2025-04-14', '23:56:23');

-- --------------------------------------------------------

--
-- Estrutura para tabela `tabelaplaca`
--

CREATE TABLE `tabelaplaca` (
  `id_placa` int(11) NOT NULL,
  `placa` varchar(7) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tabelaplaca`
--

INSERT INTO `tabelaplaca` (`id_placa`, `placa`, `usuario_id`) VALUES
(1, 'NEXTLVL', 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `tabelausuario`
--

CREATE TABLE `tabelausuario` (
  `id_usuario` int(11) NOT NULL,
  `nome` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tabelausuario`
--

INSERT INTO `tabelausuario` (`id_usuario`, `nome`) VALUES
(1, 'Rafael');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `tabelaadm`
--
ALTER TABLE `tabelaadm`
  ADD PRIMARY KEY (`id_adm`);

--
-- Índices de tabela `tabelafoto`
--
ALTER TABLE `tabelafoto`
  ADD PRIMARY KEY (`id_foto`),
  ADD KEY `pk_usuario2` (`usuario_id`);

--
-- Índices de tabela `tabelahistorico`
--
ALTER TABLE `tabelahistorico`
  ADD PRIMARY KEY (`id_historico`),
  ADD KEY `pk_placa` (`placa_id`);

--
-- Índices de tabela `tabelaplaca`
--
ALTER TABLE `tabelaplaca`
  ADD PRIMARY KEY (`id_placa`),
  ADD KEY `pk_usuario` (`usuario_id`);

--
-- Índices de tabela `tabelausuario`
--
ALTER TABLE `tabelausuario`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `tabelaadm`
--
ALTER TABLE `tabelaadm`
  MODIFY `id_adm` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `tabelafoto`
--
ALTER TABLE `tabelafoto`
  MODIFY `id_foto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `tabelahistorico`
--
ALTER TABLE `tabelahistorico`
  MODIFY `id_historico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `tabelaplaca`
--
ALTER TABLE `tabelaplaca`
  MODIFY `id_placa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `tabelausuario`
--
ALTER TABLE `tabelausuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `tabelafoto`
--
ALTER TABLE `tabelafoto`
  ADD CONSTRAINT `pk_usuario2` FOREIGN KEY (`usuario_id`) REFERENCES `tabelausuario` (`id_usuario`) ON DELETE CASCADE;

--
-- Restrições para tabelas `tabelahistorico`
--
ALTER TABLE `tabelahistorico`
  ADD CONSTRAINT `pk_placa` FOREIGN KEY (`placa_id`) REFERENCES `tabelaplaca` (`id_placa`) ON UPDATE CASCADE;

--
-- Restrições para tabelas `tabelaplaca`
--
ALTER TABLE `tabelaplaca`
  ADD CONSTRAINT `pk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `tabelausuario` (`id_usuario`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
