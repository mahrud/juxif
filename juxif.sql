-- phpMyAdmin SQL Dump
-- version 3.5.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 21, 2013 at 02:51 AM
-- Server version: 5.5.30
-- PHP Version: 5.4.12

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `juxif`
--

-- --------------------------------------------------------

--
-- Table structure for table `contests`
--

DROP TABLE IF EXISTS `contests`;
CREATE TABLE IF NOT EXISTS `contests` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `title` varchar(128) NOT NULL,
  `mode` int(11) NOT NULL,
  `begin` datetime NOT NULL,
  `length` time NOT NULL,
  `perm` int(11) NOT NULL,
  `pset` varchar(128) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cid`),
  UNIQUE KEY `cid` (`cid`),
  KEY `cid_2` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `shots`
--

DROP TABLE IF EXISTS `shots`;
CREATE TABLE IF NOT EXISTS `shots` (
  `subid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `cid` int(11) NOT NULL,
  `addr` varchar(128) NOT NULL,
  `lang` varchar(32) NOT NULL,
  `mode` int(11) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `access` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modify` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `stat` int(11) NOT NULL,
  `time` float NOT NULL,
  `mmem` int(11) NOT NULL,
  PRIMARY KEY (`subid`),
  UNIQUE KEY `subid` (`subid`),
  KEY `subid_2` (`subid`),
  KEY `subid_3` (`subid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `gid` int(11) NOT NULL,
  `username` varchar(32) NOT NULL,
  `realname` varchar(32) NOT NULL,
  `password` varchar(128) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `access` datetime NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `uid` (`uid`),
  KEY `uid_2` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
