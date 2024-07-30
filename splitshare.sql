-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 30, 2024 at 07:09 PM
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
-- Table structure for table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `activity` varchar(255) NOT NULL,
  `activity_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `room_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity_logs`
--

INSERT INTO `activity_logs` (`id`, `username`, `activity`, `activity_time`, `room_id`) VALUES
(33, 'nini', 'You created the group nicole', '2024-07-29 06:41:52', NULL),
(34, 'nini', 'You created the group nicole', '2024-07-29 06:42:06', NULL),
(35, 'miggy', 'You created the group group1', '2024-07-29 07:46:09', NULL),
(36, 'miggy', 'miggy joined the group group1 (room_id 1722239169)', '2024-07-29 07:46:49', 1722239169),
(37, 'lou', 'lou joined the group group1 (room_id 1722239169)', '2024-07-29 07:49:50', 1722239169),
(38, 'lou', 'lou joined the group group1 (room_id 1722239169)', '2024-07-29 07:49:50', 1722239169),
(39, 'lou', 'lou joined the group group1 (room_id 1722239169)', '2024-07-29 07:49:50', 1722239169),
(40, 'miggy', 'miggy added an expense of ₱100.0 for Food in group group1 (room_id 1722239169)', '2024-07-29 07:52:28', 1722239169),
(41, 'miggy', 'miggy added an expense of ₱300.0 for Fare in group group1 (room_id 1722239169)', '2024-07-29 07:52:45', 1722239169),
(42, 'gelay', 'You created the group enha', '2024-07-29 14:26:11', NULL),
(43, 'miggy', 'You created the group gogo', '2024-07-30 16:39:36', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `debts`
--

CREATE TABLE `debts` (
  `id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `lender` varchar(255) DEFAULT NULL,
  `borrower` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `debts`
--

INSERT INTO `debts` (`id`, `room_id`, `lender`, `borrower`, `amount`, `description`) VALUES
(45, 1722239169, 'miggy', 'lou', 50.00, 'Food'),
(46, 1722239169, 'lou', 'miggy', 150.00, 'Fare');

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

CREATE TABLE `expenses` (
  `id` int(11) NOT NULL,
  `room_id` int(10) UNSIGNED NOT NULL,
  `description` varchar(225) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `paid_by` varchar(225) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`id`, `room_id`, `description`, `amount`, `paid_by`, `created_at`) VALUES
(25, 1722239169, 'Food', 100.00, 'miggy', '2024-07-30 06:44:56'),
(26, 1722239169, 'Fare', 300.00, 'lou', '2024-07-30 06:44:56');

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
(64, 1722235312, 'nini'),
(65, 1722235326, 'nini'),
(66, 1722239169, 'miggy'),
(67, 1722239169, 'lou'),
(68, 1722263171, 'gelay'),
(69, 1722357576, 'miggy');

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
('marga@gmail.com', 'marga', 'marga'),
('mica@gmail.com', 'mica', 'mica'),
('micang@gmail.com', 'micang', 'micang'),
('mics@gmail.com', 'mics', 'mics'),
('panyang@gmail.com', 'panyang', 'panyang'),
('yanang@gmail.com', 'yanang', 'yanang'),
('lisa@gmail.com', 'lisa', 'lisa'),
('jennie@gmail.com', 'jennie', 'jennie'),
('jisoo@gmail.com', 'jisoo', 'jisoo'),
('rose@gmail.com', 'Rosé', 'rose'),
('kuku@gmail.com', 'kuku', 'kuku'),
('jk@gmail.com', 'jk', 'jkjk'),
('jin@gmail.com', 'jin', 'jinjin'),
('rm@gamil.com', 'rm', 'rmrm'),
('miggy@gmail.com', 'miggy', 'miggy1520'),
('lou@gmail.com', 'lou', '12345'),
('suga@gmail.com', 'suga', 'suga');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `group_name` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `creator` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id`, `room_id`, `group_name`, `username`, `creator`, `created_at`) VALUES
(26, 1722235312, 'nicole', 'nini', 'nini', '2024-07-30 16:19:09'),
(27, 1722235326, 'nicole', 'nini', 'nini', '2024-07-30 16:19:09'),
(28, 1722239169, 'group1', 'miggy', 'miggy', '2024-07-30 16:19:09'),
(29, 1722263171, 'enha', 'gelay', 'gelay', '2024-07-30 16:19:09'),
(30, 1722357576, 'gogo', 'miggy', 'miggy', '2024-07-30 16:39:36');

-- --------------------------------------------------------

--
-- Table structure for table `settlements`
--

CREATE TABLE `settlements` (
  `id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `payer` varchar(255) NOT NULL,
  `recipient` varchar(255) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `date` date NOT NULL,
  `payment_method` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`);

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
  ADD PRIMARY KEY (`id`) USING BTREE,
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
-- Indexes for table `settlements`
--
ALTER TABLE `settlements`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `debts`
--
ALTER TABLE `debts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `settlements`
--
ALTER TABLE `settlements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
