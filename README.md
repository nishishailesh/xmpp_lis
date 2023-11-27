# xmpp_lis
Python script to read a database and send mesages via XMPP protocol

#Table required
CREATE TABLE `im_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `send_to` varchar(50) DEFAULT NULL,
  `message` varchar(5000) DEFAULT NULL,
  `message_status` int(1) DEFAULT NULL,
  `recording_time` datetime DEFAULT NULL,
  `recorded_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
)
