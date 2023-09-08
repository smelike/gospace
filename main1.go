package test

import (
	"log"
	"github.com/tarm/serial"
	"time"
)

func main() {
	c := &serial.Config{Name: "COM21", Baud: 19200}
	
	s, err := serial.OpenPort(c)
	
	if err != nil {
		log.Printf("serial port open error: %v", err)
	}
	
	n, err := s.Write([]byte("010300500002c41a"))
	log.Printf("writen %v byte", n)
	if err != nil {
		log.Printf("Write error: %v", err)
	}
	
	
	time.Sleep(2 * time.Second)
	var resp []byte
	b, err := s.Read(resp)
	log.Printf("data: %q", b)
	
	time.Sleep(2 * time.Second)
	b, err = s.Read(resp)
	log.Printf("data: %q", b)
	
	/*
	buf := make([]byte, 128)
	for {
		log.Printf(time.Now())
		log.Printf("Please wait, reading data...")
		time.Sleep(20 * time.Millisecond)
		n, err = s.Read(buf)
		log.Printf("Read %v bytes data", n)
		log.Printf("Data %v", buf)
		if err != nil {
			log.Fatal("Read error: %v", err)
		}
		log.Printf("Read Data: %q", buf[:n])
	}
	*/
	
	buf := make([]byte, 128)
	n, err = s.Read(buf)
	if err != nil {
		  log.Fatal(err)
	}
	log.Print("%q", buf[:n])
}