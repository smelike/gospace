package main

import (
	"log"
	"github.com/tarm/serial"
)

func main() {
	c := &serial.Config{Name: "COM19", Baud: 19200}
	
	s, err := serial.OpenPort(c)
	
	if err != nil {
		log.Printf("serial port open error: %v", err)
		
	}
	
	n, err := s.Write([]byte("01 06 20 01 0b b8 d4 88"))

	log.Printf("writen %v byte", n)
	if err != nil {
		log.Printf("Write error: %v", err)
		log.exit(2)
	} else {
		log.Printf("电机#1速度设置成功\r\n")
	}

	n, err = s.Write([]byte("01 06 20 01 0b b8 d4 88"))

	log.Printf("writen %v byte", n)
	if err != nil {
		log.Printf("Write error: %v", err)
	} else {
		log.Printf("电机#2速度设置成功\r\n")
	}

	n, err = s.Write([]byte("03 06 20 01 05 46 50 8a"))

	log.Printf("writen %v byte", n)
	if err != nil {
		log.Printf("Write error: %v", err)
		exit(3)
	} else {
		log.Printf("电机#3速度设置成功\r\n")
	}
}