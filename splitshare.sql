-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 02, 2024 at 05:38 PM
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
(39, 'lou', 'lou joined the group group1 (room_id 1722239169)', '2024-07-29 07:49:50', 1722239169),
(40, 'miggy', 'miggy added an expense of ₱100.0 for Food in group group1 (room_id 1722239169)', '2024-07-29 07:52:28', 1722239169),
(41, 'miggy', 'miggy added an expense of ₱300.0 for Fare in group group1 (room_id 1722239169)', '2024-07-29 07:52:45', 1722239169),
(42, 'gelay', 'You created the group enha', '2024-07-29 14:26:11', NULL),
(43, 'miggy', 'You created the group gogo', '2024-07-30 16:39:36', NULL),
(44, 'miggy', 'Ended the group with room_id 1722357576', '2024-07-30 17:15:55', NULL),
(45, 'lou', 'lou joined the group gogo (room_id 1722357576)', '2024-07-30 17:20:16', 1722357576),
(46, 'miggy', 'You created the group barda', '2024-07-30 17:31:14', NULL),
(47, 'miggy', 'Ended the group \'barda\' (room_id: 1722360674)', '2024-07-30 17:31:50', NULL),
(48, 'miggy', 'created a group named \'ano (room_id: 1722361434)', '2024-07-30 17:43:54', 1722361434),
(49, 'miggy', 'Ended the group \'ano\' (room_id: 1722361434)', '2024-07-30 17:44:35', 1722361434),
(50, 'miggy', 'created a group named \'huh (room_id: 1722363954)', '2024-07-30 18:25:54', 1722363954),
(51, 'lou', 'lou joined the group huh (room_id 1722363954)', '2024-07-30 18:26:39', 1722363954),
(52, 'miggy', 'miggy added an expense of ₱1400.0 for food in group huh (room_id 1722363954)', '2024-07-30 18:27:40', 1722363954),
(53, 'lisa', 'created a group named \'biya (room_id: 1722364557)', '2024-07-30 18:35:57', 1722364557),
(54, 'Rosé', 'Rosé joined the group biya (room_id 1722364557)', '2024-07-30 18:36:47', 1722364557),
(55, 'lisa', 'created a group named \'biyaya (room_id: 1722364770)', '2024-07-30 18:39:30', 1722364770),
(56, 'Rosé', 'Rosé joined the group biyaya (room_id 1722364770)', '2024-07-30 18:46:23', 1722364770),
(57, 'lisa', 'lisa added an expense of ₱3400.0 for food in group biyaya (room_id 1722364770)', '2024-07-30 19:06:13', 1722364770),
(58, 'lisa', 'You ended the group \'biyaya\' (room_id: 1722364770)', '2024-07-30 19:06:29', NULL),
(59, 'Rosé', 'created a group named \'bpinks (room_id: 1722366900)', '2024-07-30 19:15:00', 1722366900),
(60, 'Rosé', 'Rosé joined the group bpinks (room_id 1722366900)', '2024-07-30 19:15:59', 1722366900),
(61, 'jisoo', 'jisoo joined the group bpinks (room_id 1722366900)', '2024-07-30 19:17:48', 1722366900),
(62, 'Rosé', 'Rosé added an expense of ₱6400.0 for food in group bpinks (room_id 1722366900)', '2024-07-30 19:18:24', 1722366900),
(63, 'Rosé', 'You ended the group \'bpinks\' (room_id: 1722366900)', '2024-07-30 19:18:40', NULL),
(64, 'jk', 'created a group named \'bangtan (room_id: 1722367276)', '2024-07-30 19:21:16', 1722367276),
(65, 'jin', 'jin joined the group bangtan (room_id 1722367276)', '2024-07-30 19:22:02', 1722367276),
(66, 'jk', 'jk added an expense of ₱45000.0 for food in group bangtan (room_id 1722367276)', '2024-07-30 19:24:10', 1722367276),
(67, 'jk', 'You ended the group \'bangtan\' (room_id: 1722367276)', '2024-07-30 19:24:19', NULL),
(68, 'jk', 'created a group named \'borahae (room_id: 1722367719)', '2024-07-30 19:28:39', 1722367719),
(69, 'rm', 'rm joined the group borahae (room_id 1722367719)', '2024-07-30 19:29:37', 1722367719),
(70, 'jk', 'jk added an expense of ₱1600.0 for food in group borahae (room_id 1722367719)', '2024-07-30 19:30:25', 1722367719),
(71, 'jk', 'You ended the group \'borahae\' (room_id: 1722367719)', '2024-07-30 19:31:13', NULL),
(72, 'jk', 'created a group named \'btss (room_id: 1722368419)', '2024-07-30 19:40:19', 1722368419),
(73, 'jin', 'jin joined the group btss (room_id 1722368419)', '2024-07-30 19:41:09', 1722368419),
(74, 'jk', 'jk added an expense of ₱4500.0 for food in group btss (room_id 1722368419)', '2024-07-30 19:41:56', 1722368419),
(75, 'jk', 'created a group named \'yokona (room_id: 1722368841)', '2024-07-30 19:47:21', 1722368841),
(76, 'lisa', 'lisa joined the group yokona (room_id 1722368841)', '2024-07-30 19:48:08', 1722368841),
(77, 'jk', 'jk added an expense of ₱7500.0 for food in group yokona (room_id 1722368841)', '2024-07-30 19:48:47', 1722368841),
(78, 'jk', 'You ended the group \'yokona\' (room_id: 1722368841)', '2024-07-30 19:49:03', 1722368841),
(79, 'gelay', 'created a group named \'mmm (room_id: 1722398729)', '2024-07-31 04:05:29', 1722398729),
(80, 'nini', 'nini joined the group mmm (room_id 1722398729)', '2024-07-31 04:15:16', 1722398729),
(81, 'gelay', 'gelay added an expense of ₱1600.0 for food in group mmm (room_id 1722398729)', '2024-07-31 04:16:05', 1722398729),
(82, 'nini', 'nini joined the group mmm (room_id 1722398729)', '2024-07-31 04:16:24', 1722398729),
(83, 'gelay', 'gelay ended the group enha (room_id: 1722263171)', '2024-07-31 04:19:00', 1722263171),
(84, 'nini', 'nini joined the group mmm (room_id 1722398729)', '2024-07-31 04:19:58', 1722398729),
(85, 'gelay', 'gelay recorded a payment from gelay to gelay in group mmm', '2024-07-31 04:24:53', 1722398729),
(86, 'gelay', 'gelay deleted the expense \'food\' in room 1722398729', '2024-07-31 04:27:17', NULL),
(87, 'gelay', 'gelay added an expense of ₱60.0 for fare in group mmm (room_id 1722398729)', '2024-07-31 04:30:30', 1722398729),
(88, 'gelay', 'gelay deleted the expense \'fare\' in room 1722398729', '2024-07-31 04:30:50', 1722398729),
(89, 'gelay', 'gelay added an expense of ₱500.0 for food in group mmm (room_id 1722398729)', '2024-07-31 04:35:45', 1722398729),
(90, 'gelay', 'gelay deleted the expense food in group mmm', '2024-07-31 04:36:01', 1722398729),
(91, 'gelay', 'gelay added an expense of ₱900.0 for food in group mmm (room_id 1722398729)', '2024-07-31 04:38:59', 1722398729),
(92, 'gelay', 'gelay edited the expense food in group mmm', '2024-07-31 04:39:37', 1722398729),
(93, 'gelay', 'gelay recorded a payment from gelay to nini in group mmm', '2024-07-31 05:42:57', 1722398729),
(94, 'gelay', 'gelay ended the group mmm (room_id: 1722398729)', '2024-07-31 05:49:07', 1722398729),
(95, 'nini', 'nini added an expense of ₱200.0 for food in group nicole (room_id 1722235326)', '2024-07-31 06:08:42', 1722235326),
(96, 'lisa', 'created a group named \'pingkuu (room_id: 1722407025)', '2024-07-31 06:23:45', 1722407025),
(97, 'Rosé', 'Rosé joined the group pingkuu (room_id 1722407025)', '2024-07-31 06:25:06', 1722407025),
(98, 'lisa', 'You added an expense of ₱5600.0 for food in group pingkuu (room_id 1722407025)', '2024-07-31 06:26:00', 1722407025),
(99, 'lisa', 'You added an expense of ₱45000.0 for fare in group pingkuu (room_id 1722407025)', '2024-07-31 06:26:23', 1722407025),
(100, 'lisa', 'created a group named \'lilies (room_id: 1722407522)', '2024-07-31 06:32:02', 1722407522),
(101, 'jisoo', 'jisoo joined the group lilies (room_id 1722407522)', '2024-07-31 06:32:44', 1722407522),
(102, 'jennie', 'jennie joined the group lilies (room_id 1722407522)', '2024-07-31 06:34:09', 1722407522),
(103, 'Rosé', 'Rosé joined the group lilies (room_id 1722407522)', '2024-07-31 06:37:23', 1722407522),
(104, 'lisa', 'You added an expense of ₱34000.0 for food in group lilies (room_id 1722407522)', '2024-07-31 06:39:18', 1722407522),
(105, 'gelay', 'created a group named \'huhu (room_id: 1722610067)', '2024-08-02 14:47:47', 1722610067),
(106, 'gelay', 'created a group named \'howww (room_id: 1722610354)', '2024-08-02 14:52:34', 1722610354),
(107, 'nini', 'nini joined the group howww (room_id 1722610354)', '2024-08-02 14:54:26', 1722610354),
(108, 'gelay', 'You added an expense of ₱50000.0 for food in group howww (room_id 1722610354)', '2024-08-02 14:55:02', 1722610354);

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
(46, 1722239169, 'lou', 'miggy', 150.00, 'Fare'),
(47, 1722363954, 'miggy', 'lou', 700.00, 'food'),
(48, 1722364770, 'Rosé', 'lisa', 1700.00, 'food'),
(49, 1722366900, 'jisoo', 'Rosé', 3200.00, 'food'),
(50, 1722367276, 'jin', 'jk', 22500.00, 'food'),
(51, 1722367719, 'rm', 'jk', 800.00, 'food'),
(52, 1722368419, 'jin', 'jk', 2250.00, 'food'),
(53, 1722368841, 'lisa', 'jk', 3750.00, 'food'),
(58, 1722398729, 'nini', 'gelay', 400.00, 'food'),
(60, 1722407025, 'Rosé', 'lisa', 22500.00, 'fare'),
(61, 1722407522, 'jisoo', 'lisa', 8500.00, 'food'),
(62, 1722407522, 'jisoo', 'jennie', 8500.00, 'food'),
(63, 1722407522, 'jisoo', 'Rosé', 8500.00, 'food'),
(64, 1722610354, 'nini', 'gelay', 25000.00, 'food');

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
(26, 1722239169, 'Fare', 300.00, 'lou', '2024-07-30 06:44:56'),
(27, 1722363954, 'food', 1400.00, 'miggy', '2024-07-30 18:27:40'),
(28, 1722364770, 'food', 3400.00, 'Rosé', '2024-07-30 19:06:13'),
(29, 1722366900, 'food', 6400.00, 'jisoo', '2024-07-30 19:18:24'),
(30, 1722367276, 'food', 45000.00, 'jin', '2024-07-30 19:24:10'),
(31, 1722367719, 'food', 1600.00, 'rm', '2024-07-30 19:30:25'),
(32, 1722368419, 'food', 4500.00, 'jin', '2024-07-30 19:41:56'),
(33, 1722368841, 'food', 7500.00, 'lisa', '2024-07-30 19:48:47'),
(37, 1722398729, 'food', 800.00, 'nini', '2024-07-31 04:38:59'),
(38, 1722235326, 'food', 200.00, 'nini', '2024-07-31 06:08:42'),
(39, 1722407025, 'food', 5600.00, 'Rosé', '2024-07-31 06:26:00'),
(40, 1722407025, 'fare', 45000.00, 'Rosé', '2024-07-31 06:26:23'),
(41, 1722407522, 'food', 34000.00, 'jisoo', '2024-07-31 06:39:18'),
(42, 1722610354, 'food', 50000.00, 'nini', '2024-08-02 14:55:02');

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
(69, 1722357576, 'miggy'),
(70, 1722357576, 'lou'),
(71, 1722360674, 'miggy'),
(72, 1722361434, 'miggy'),
(73, 1722363954, 'miggy'),
(74, 1722363954, 'lou'),
(75, 1722364557, 'lisa'),
(76, 1722364557, 'Rosé'),
(77, 1722364770, 'lisa'),
(78, 1722364770, 'Rosé'),
(79, 1722366900, 'Rosé'),
(80, 1722366900, 'jisoo'),
(81, 1722367276, 'jk'),
(82, 1722367276, 'jin'),
(83, 1722367719, 'jk'),
(84, 1722367719, 'rm'),
(85, 1722368419, 'jk'),
(86, 1722368419, 'jin'),
(87, 1722368841, 'jk'),
(88, 1722368841, 'lisa'),
(89, 1722398729, 'gelay'),
(90, 1722398729, 'nini'),
(91, 1722407025, 'lisa'),
(92, 1722407025, 'Rosé'),
(93, 1722407522, 'lisa'),
(94, 1722407522, 'jisoo'),
(95, 1722407522, 'jennie'),
(96, 1722407522, 'Rosé'),
(97, 1722610067, 'gelay'),
(98, 1722610354, 'gelay'),
(99, 1722610354, 'nini');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `address` varchar(500) NOT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `instagram` varchar(500) DEFAULT NULL,
  `facebook` varchar(500) DEFAULT NULL,
  `twitter` varchar(500) DEFAULT NULL,
  `github` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `email`, `username`, `password`, `first_name`, `last_name`, `phone_number`, `address`, `profile_picture`, `instagram`, `facebook`, `twitter`, `github`) VALUES
(1, 'nicole@gmail.com', 'nini', '123456', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(2, 'nicolemahilum2@gmail.com', 'nicole', '987456', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(3, 'nini@gmail.com', 'niks', '456654', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(4, 'lou@gmail.com', 'lou', '123456789', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(5, 'gelay@gmail.com', 'gelay', '0828', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(6, 'miggy@churba', 'migi', 'migi', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(7, 'MharianLover@nicole.com', 'MharianXNicole', 'nini', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(8, 'preciouskim@gmail.com', 'kimiekims', 'precious', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(9, 'matcha@gmail.com', 'matcha', 'matcha', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(10, 'moo@gmail.com', 'moo', 'moomoo', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(11, 'marga@gmail.com', 'marga', 'marga', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(12, 'mica@gmail.com', 'mica', 'mica', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(13, 'micang@gmail.com', 'micang', 'micang', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(14, 'mics@gmail.com', 'mics', 'mics', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(15, 'panyang@gmail.com', 'panyang', 'panyang', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(16, 'yanang@gmail.com', 'yanang', 'yanang', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(17, 'lisa@gmail.com', 'lisa', 'lisa', 'lalisa', 'manobal', '143', 'Thailand', 'static/uploads\\lisa_foto.jpg', 'https://www.instagram.com/lalalalisa_m/', 'None', 'None', 'None'),
(18, 'jennie@gmail.com', 'jennie', 'jennie', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(19, 'jisoo@gmail.com', 'jisoo', 'jisoo', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(20, 'rose@gmail.com', 'Rosé', 'rose', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(21, 'kuku@gmail.com', 'kuku', 'kuku', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(22, 'jk@gmail.com', 'jk', 'jkjk', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(23, 'jin@gmail.com', 'jin', 'jinjin', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(24, 'rm@gamil.com', 'rm', 'rmrm', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(25, 'miggy@gmail.com', 'miggy', 'miggy1520', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(26, 'lou@gmail.com', 'lou', '12345', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(27, 'suga@gmail.com', 'suga', 'suga', '', '', '', '', NULL, NULL, NULL, NULL, NULL),
(28, 'lala@gmail.com', 'lala', 'scrypt:32768:8:1$RNmiGYTmpOpkV6vI$8259b7530f9bf126', 'lala', 'manobal', '09123456789', '', NULL, NULL, NULL, NULL, NULL),
(29, 'zuma@gmail.com', 'zuma', 'scrypt:32768:8:1$roqeFHhfPXpAdTxW$0ceb53b880587f5c', 'zuma', 'langit', '09987456321', '', NULL, NULL, NULL, NULL, NULL),
(30, 'sasa@gmail.com', 'sasa', 'sasa', 'sasa', 'girl', '09888888888', '', NULL, NULL, NULL, NULL, NULL),
(31, 'asa@gmail.com', 'asa', 'asabm', 'asa', 'kim', '09321456987', '', 'static/uploads\\asa.jpg', NULL, NULL, NULL, NULL),
(32, 'rami@gmail.com', 'ramibaby', 'ramibm', 'rami', 'haram', '09111111111', 'Seoul, SK', NULL, NULL, NULL, NULL, NULL),
(33, 'chiquita@gmail.com', 'Chiquita', 'chiquitabm', 'Chiquita', 'love', '09222222222', '', NULL, NULL, NULL, NULL, NULL),
(34, 'ruka@gmail.com', 'ruka', 'rukabm', 'ruka', 'kawai', '09444444444', '', NULL, NULL, NULL, NULL, NULL);

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
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_active` tinyint(1) DEFAULT 1,
  `ended_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id`, `room_id`, `group_name`, `username`, `creator`, `created_at`, `is_active`, `ended_at`) VALUES
(26, 1722235312, 'nicole', 'nini', 'nini', '2024-07-30 16:19:09', 1, NULL),
(27, 1722235326, 'nicole', 'nini', 'nini', '2024-07-30 16:19:09', 1, NULL),
(28, 1722239169, 'group1', 'miggy', 'miggy', '2024-07-30 16:19:09', 1, NULL),
(29, 1722263171, 'enha', 'gelay', 'gelay', '2024-07-30 16:19:09', 0, '2024-07-31 04:19:00'),
(30, 1722357576, 'gogo', 'miggy', 'miggy', '2024-07-30 16:39:36', 0, NULL),
(31, 1722360674, 'barda', 'miggy', 'miggy', '2024-07-30 17:31:14', 0, NULL),
(32, 1722361434, 'ano', 'miggy', 'miggy', '2024-07-30 17:43:54', 0, NULL),
(33, 1722363954, 'huh', 'miggy', 'miggy', '2024-07-30 18:25:54', 0, '2024-07-30 18:30:10'),
(34, 1722364557, 'biya', 'lisa', 'lisa', '2024-07-30 18:35:57', 0, '2024-07-30 18:37:30'),
(35, 1722364770, 'biyaya', 'lisa', 'lisa', '2024-07-30 18:39:30', 0, '2024-07-30 19:06:29'),
(36, 1722366900, 'bpinks', 'Rosé', 'Rosé', '2024-07-30 19:15:00', 0, '2024-07-30 19:18:40'),
(37, 1722367276, 'bangtan', 'jk', 'jk', '2024-07-30 19:21:16', 0, '2024-07-30 19:24:19'),
(38, 1722367719, 'borahae', 'jk', 'jk', '2024-07-30 19:28:39', 0, '2024-07-30 19:31:13'),
(39, 1722368419, 'btss', 'jk', 'jk', '2024-07-30 19:40:19', 0, '2024-07-30 19:42:08'),
(40, 1722368841, 'yokona', 'jk', 'jk', '2024-07-30 19:47:21', 0, '2024-07-30 19:49:03'),
(41, 1722398729, 'mmm', 'gelay', 'gelay', '2024-07-31 04:05:29', 0, '2024-07-31 05:49:07'),
(42, 1722407025, 'pingkuu', 'lisa', 'lisa', '2024-07-31 06:23:45', 1, NULL),
(43, 1722407522, 'lilies', 'lisa', 'lisa', '2024-07-31 06:32:02', 1, NULL),
(44, 1722610067, 'huhu', 'gelay', 'gelay', '2024-08-02 14:47:47', 1, NULL),
(45, 1722610354, 'howww', 'gelay', 'gelay', '2024-08-02 14:52:34', 1, NULL);

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
-- Dumping data for table `settlements`
--

INSERT INTO `settlements` (`id`, `room_id`, `payer`, `recipient`, `amount`, `date`, `payment_method`) VALUES
(6, 1722367719, 'jk', 'rm', 600.00, '2024-07-31', 'e-wallet'),
(7, 1722398729, 'gelay', 'nini', 200.00, '2024-08-02', 'cash'),
(8, 1722398729, 'gelay', 'gelay', 200.00, '2024-08-02', 'cash'),
(9, 1722398729, 'gelay', 'nini', 100.00, '2024-08-08', 'e-wallet');

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
-- Indexes for table `register`
--
ALTER TABLE `register`
  ADD PRIMARY KEY (`id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=109;

--
-- AUTO_INCREMENT for table `debts`
--
ALTER TABLE `debts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;

--
-- AUTO_INCREMENT for table `register`
--
ALTER TABLE `register`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `settlements`
--
ALTER TABLE `settlements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
