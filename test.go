package main


import (
	"fmt"
	"log"
	//"strings"
	"time"
	"encoding/hex"
	"go.bug.st/serial"
)


func main() {

	ports, err := serial.GetPortsList()
	
	if err != nil {
		log.Fatal(err)
	}
	
	if len(ports) == 0 {
		log.Fatal("No serial ports found!")
	}
	
	for _, port := range ports {
		fmt.Printf("Found port: %v\n", port)
	}
	
	// Open the first serial port detected at 9600bps 
	mode := &serial.Mode{
		BaudRate: 19200,
		Parity: serial.NoParity,
		DataBits: 8,
		StopBits: serial.OneStopBit,
	}
	port, err := serial.Open(ports[0], mode)
	if err != nil {
		log.Fatal(err)
	}
	
	// send the string "10, 20, 30\n\r" to the serial port
	// 010300500002c41a
	// n, err := port.Write([]byte("\x01\x03\x00\x50\x00\x02\xc4\x1a"))
	n, err := port.Write([]byte("\x01\x03\x00\x50\x00\x02\xc4\x1a"))
	
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Sent %v bytes\n", n)
	
	// Read and print the response
	
	buff := make([]byte, 100)
	
	time.Sleep(time.Second/2)

    //buf := make([]byte, 40)
    n, err = port.Read(buff)
	//fmt.Printf("the length of return data: %d", n)
	fmt.Println(buff[:n])
	
	// 01 03 04 00 00 00 00 FA 33 
	encodeHex := hex.EncodeToString(buff[:n])
	fmt.Print(encodeHex)

    if err != nil {
        fmt.Println(err)
    }

    //fmt.Println(string(buff[:n]))

    port.Close()
	/*
	for {
		// Reads up to 100 bytes
		log.Print("Into for loop..")
		time.Sleep(500 * time.Millisecond)
		n, err := port.Read(buff)
		log.Printf("n is %v\n", n)
		if err != nil {
			log.Fatal(err)
		}
		if n == 0 {
			fmt.Println("\nEOF")
			break
		}
		
		
		// if we receive a newline stop reading
		if strings.Contains(string(buff[:n]), "\n") {
			break
		}
	}
	
	*/
	// fmt.Printf("%s", string(buff[:n]))
}