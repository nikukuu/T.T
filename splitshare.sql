-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 22, 2024 at 04:34 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `splitshare`
--

-- --------------------------------------------------------

--
-- Table structure for table `debts`
--

CREATE TABLE `debts` (
  `id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `lender` varchar(255) DEFAULT NULL,
  `borrower` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `debts`
--

INSERT INTO `debts` (`id`, `room_id`, `lender`, `borrower`, `amount`) VALUES
(3, 1721393726, 'gelay', 'lou', 300.00),
(4, 1721393726, 'gelay', 'nini', 300.00),
(5, 1721393726, 'gelay', 'migi', 300.00),
(6, 1721393726, 'migi', 'lou', 750.00),
(7, 1721393726, 'migi', 'gelay', 750.00),
(8, 1721393726, 'migi', 'nini', 750.00),
(9, 1721393726, 'nini', 'lou', 290.00),
(10, 1721393726, 'nini', 'gelay', 290.00),
(11, 1721393726, 'nini', 'migi', 290.00),
(12, 1721654937, 'moo', 'matcha', 1666.67),
(13, 1721654937, 'moo', 'marga', 1666.67),
(14, 1721654937, 'matcha', 'moo', 1000.00),
(15, 1721654937, 'matcha', 'marga', 1000.00),
(16, 1721654937, 'marga', 'matcha', 833.33),
(17, 1721654937, 'marga', 'moo', 833.33);

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

CREATE TABLE `expenses` (
  `id` int(11) NOT NULL,
  `room_id` int(10) UNSIGNED NOT NULL,
  `description` varchar(225) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `paid_by` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`id`, `room_id`, `description`, `amount`, `paid_by`) VALUES
(1, 1721206218, 'Food', 500.00, 'lou'),
(2, 1721206218, 'Fare', 60.00, 'nicole'),
(5, 1721393726, 'Food', 1200.00, 'gelay'),
(6, 1721393726, 'Bar', 3000.00, 'migi'),
(7, 1721393726, 'Tickets', 1160.00, 'nini'),
(8, 1721654937, 'dog food', 5000.00, 'moo'),
(9, 1721654937, 'treats', 3000.00, 'matcha'),
(10, 1721654937, 'grooming', 2500.00, 'marga');

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `username` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`id`, `room_id`, `username`) VALUES
(1, 1721109537, 'gelay'),
(2, 1721112345, 'nini'),
(3, 1721112345, 'lou'),
(4, 1721112345, 'niks'),
(5, 1721146693, 'nini'),
(6, 1721148278, 'nini'),
(7, 1721148278, 'gelay'),
(8, 1721148278, 'lou'),
(9, 1721148639, 'gelay'),
(10, 1721148639, 'nicole'),
(11, 1721148639, 'lou'),
(12, 1721182538, 'gelay'),
(13, 1721182538, 'nini'),
(14, 1721182538, 'migi'),
(15, 1721182538, 'lou'),
(16, 1721205745, 'nini'),
(17, 1721205745, 'gelay'),
(18, 1721205745, 'migi'),
(19, 1721205745, 'lou'),
(20, 1721206218, 'nicole'),
(21, 1721206218, 'gelay'),
(22, 1721206218, 'lou'),
(23, 1721206218, 'migi'),
(24, 1721393726, 'lou'),
(25, 1721393726, 'gelay'),
(26, 1721393726, 'nini'),
(27, 1721393726, 'migi'),
(28, 1721454068, 'kimiekims'),
(29, 1721454068, 'nini'),
(30, 1721653386, 'matcha'),
(31, 1721654937, 'matcha'),
(32, 1721654937, 'moo'),
(33, 1721654937, 'marga');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `email` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`email`, `username`, `password`) VALUES
('nicole@gmail.com', 'nini', '123456'),
('nicolemahilum2@gmail.com', 'nicole', '987456'),
('nini@gmail.com', 'niks', '456654'),
('lou@gmail.com', 'lou', '123456789'),
('gelay@gmail.com', 'gelay', '0828'),
('miggy@churba', 'migi', 'migi'),
('MharianLover@nicole.com', 'MharianXNicole', 'nini'),
('preciouskim@gmail.com', 'kimiekims', 'precious'),
('matcha@gmail.com', 'matcha', 'matcha'),
('moo@gmail.com', 'moo', 'moomoo'),
('marga@gmail.com', 'marga', 'marga');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `group_name` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id`, `room_id`, `group_name`, `username`) VALUES
(1, 1721146693, 'group1', 'gelay'),
(2, 1721148278, 'group2', ''),
(3, 1721148639, 'groupko', ''),
(4, 1721182538, 'uwu', 'gelay'),
(5, 1721205745, 'riserts', 'nini'),
(6, 1721206218, 'elyu', 'nicole'),
(7, 1721393726, 'wjc', 'lou'),
(8, 1721454068, 'odccccc', 'kimiekims'),
(9, 1721653386, 'milktea', 'matcha'),
(10, 1721654937, 'LCvit', 'matcha');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `debts`
--
ALTER TABLE `debts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_debt` (`room_id`,`lender`,`borrower`);

--
-- Indexes for table `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`id`),
  ADD KEY `index_username` (`username`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `debts`
--
ALTER TABLE `debts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
