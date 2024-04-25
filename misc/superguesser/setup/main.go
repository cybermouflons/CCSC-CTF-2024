package main

import (
	"bufio"
	"fmt"
	"math"
	"math/rand"
	"net"
	"os"
	"strconv"
	"strings"
	"time"
)

var flags []string

func init() {
	flag_one := os.Getenv("FLAG_ONE")
	if flag_one == "" {
		flag_one = "CCSC{fake_dummy_flag_1}"
	}

	flag_two := os.Getenv("FLAG_TWO")
	if flag_two == "" {
		flag_two = "CCSC{fake_dummy_flag_2}"
	}

	flag_three := os.Getenv("FLAG_THREE")
	if flag_three == "" {
		flag_three = "CCSC{fake_dummy_flag_3}"
	}

	flags = []string{flag_one, flag_two, flag_three}
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "7945"
	}
	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		return
	}
	defer listener.Close()

	fmt.Println("Listening on port " + port)

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err.Error())
			return
		}

		fmt.Println("Client connected")

		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	gen := func(part int) (randomNumber int64, maxTries int) {
		switch part {
		case 1:
			seed := time.Now().Unix()
			random := rand.New(rand.NewSource(seed))
			randomNumber, maxTries = random.Int63(), 10
			return
		case 2:
			seed := time.Now().UnixMilli()
			random := rand.New(rand.NewSource(seed))
			randomNumber, maxTries = random.Int63(), 50
			return
		case 3:
			seed := time.Now().UnixNano()
			random := rand.New(rand.NewSource(seed))
			randomNumber, maxTries = random.Int63(), 100
			return
		}
		return 0, 0
	}

	reader := bufio.NewReader(conn)
	writer := bufio.NewWriter(conn)

	writer.WriteString("v1.1\n")
	writer.WriteString("=======================================================\n")
	writer.WriteString("ReverseCAPTCHA commencing... Prove you are not a human!\n")
	writer.WriteString("=======================================================\n\n")
	writer.Flush()

	var optionSelected = -1

	for {
		writer.WriteString("Options:\n--------\n(1) Part One\n(2) Part Two\n(3) Part Three\n\nSolve part: ")
		writer.Flush()

		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading input:", err.Error())
			return
		}

		input = strings.TrimSpace(input)
		option, err := strconv.Atoi(input)
		if err != nil || option > 3 || option < 1 {
			writer.WriteString("\n[x] Invalid input.\n\n")
			writer.Flush()
			continue
		}

		optionSelected = option
		break
	}

	randomNumber, maxTries := gen(optionSelected)
	if randomNumber == 0 {
		fmt.Println("Something's wrong, terminate")
		return
	}

	triesLeft := maxTries

	writer.WriteString("\n")
	writer.WriteString(fmt.Sprintf("I've hallucinated a number between 0 and %d. Can you guess it?\n\n", math.MaxInt64))
	writer.WriteString(fmt.Sprintf("You have %d tries.\n\n", maxTries))
	writer.Flush()

	for {
		writer.WriteString(fmt.Sprintf("[%d]: ", triesLeft))
		writer.Flush()

		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading input:", err.Error())
			return
		}

		input = strings.TrimSpace(input)
		guess, err := strconv.ParseInt(input, 10, 64)
		if err != nil {
			writer.WriteString("Invalid input.\n")
			writer.Flush()
			continue
		}

		triesLeft--

		if triesLeft <= 0 {
			writer.WriteString("\nBye.\n")
			writer.Flush()
			return
		} else if guess < randomNumber {
			writer.WriteString("++ Higher\n")
			writer.Flush()
		} else if guess > randomNumber {
			writer.WriteString("-- Lower\n")
			writer.Flush()
		} else {
			writer.WriteString(fmt.Sprintf("Superior computational brain power detected.\n%s\n", flags[optionSelected-1]))
			writer.Flush()
			return
		}
	}
}
