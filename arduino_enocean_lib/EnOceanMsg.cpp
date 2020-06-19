/*
  EnOceanMsg.cpp - Library for flashing EnOceanMsg code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/

#include "Arduino.h"
#include "EnOceanMsg.h"

EnOceanMsg::EnOceanMsg()
{
  reset();
}

void EnOceanMsg::reset()
{
  _dataLength1 = 0;
  _dataLength2 = 0;
  _optLength = 0;
  _packetType = 0;
  _headerCrc8 = 0;
  _org = 0;
  _payload = 0;
  _senderId1 = 0;
  _senderId2 = 0;
  _senderId3 = 0;
  _senderId4 = 0;
  _dataReceived = false;
}

uint16_t EnOceanMsg::getPacketLength() {
    //_dataLength1=0x45;
    //_dataLength2=0xA1;
	return ((uint16_t(_dataLength1) << 8) & 0xffff) + (_dataLength2 & 0xff);
}

int EnOceanMsg::getPayload(){
return _payload;
}

bool EnOceanMsg::dataAvailable()
{
return _dataReceived;
}

uint32_t EnOceanMsg::getSenderId() {
    //_senderId1=0x45;
    //_senderId2=0x46;
    //_senderId3=0x47;
    //_senderId4=0x48;
    uint32_t aResponse = ((uint32_t(_senderId1) << 24) & 0xffffffff) + ((uint32_t(_senderId2)  << 16) & 0xffffffff) + ((uint32_t(_senderId3) << 8) & 0xffffffff) + (uint32_t(_senderId4) & 0xffffffff);
	return aResponse;
}

void EnOceanMsg::prettyPrint()
{
Serial.println("Pretty print start");

Serial.print("length:");
char buf1[9];
sprintf(buf1, "%04x", getPacketLength());
Serial.println(buf1);
//Serial.println(getPacketLength());

Serial.print("Optional length:");
Serial.println(_optLength);

Serial.print("Packet type:0x");
Serial.println(_packetType, HEX);

Serial.print("ORG:0x");
Serial.println(_org, HEX);

Serial.print("Payload:0x");
Serial.println(_payload, HEX);

Serial.print("Sender Id:");
char buf[20];
sprintf(buf, "%lx", getSenderId());
Serial.println(buf);
//Serial.println(getSenderId(), HEX);

Serial.println("Pretty print end");
}

void EnOceanMsg::decode()
{
  //Serial.println("Entering");
  while(Serial1.available() > 0)
  {
  //Serial.println("Decoding");
  _dataReceived=true;
    uint8_t aChar = Serial1.read();
    switch(_pos) 
  {
			case 0:
		        if (aChar == START_BYTE) 
                {
		        	_pos++;
                    //Serial.println("START");
		        }
                break;
                
                case 1:
				// length msb
				_dataLength1=aChar;
				_pos++;
                //Serial.print("length msb:");
                //Serial.println(_dataLength1, HEX);
				break;
                
			case 2:
				// length lsb
				_dataLength2=aChar;
				_pos++;
                //Serial.print("length lsb:");
                //Serial.println(_dataLength2, HEX);
				break;
                
                case 3:
				// length lsb
				_optLength=aChar;
				_pos++;
                //Serial.print("_optLength lsb:");
                //Serial.println(_optLength, HEX);
				break;
                
                case 4:
				// length lsb
				_packetType=aChar;
				_pos++;
                //Serial.print("_packetType lsb:");
                //Serial.println(_packetType, HEX);
				break;
                
                case 5:
				// length lsb
				_headerCrc8=aChar;
				_pos++;
                //Serial.print("_headerCrc8 lsb:");
                //Serial.println(_headerCrc8, HEX);
				break;
                
                case 6:
				// length lsb
				_org=aChar;
				_pos++;
                //Serial.print("_headerCrc8 lsb:");
                //Serial.println(_headerCrc8, HEX);
				break;
                
                case 7:
				// length lsb
				_payload=aChar;
				_pos++;
                //Serial.print("_headerCrc8 lsb:");
                //Serial.println(_headerCrc8, HEX);
				break;
                
                
                case 8:
				_senderId1=aChar;
				_pos++;
                //Serial.print("_senderId1:");
                //Serial.println(_senderId1, HEX);
				break;
                
                case 9:
				_senderId2=aChar;
				_pos++;
                //Serial.print("_senderId2:");
                //Serial.println(_senderId2, HEX);
				break;
                
                case 10:
				_senderId3=aChar;
				_pos++;
                //Serial.print("_senderId3:");
                //Serial.println(_senderId3, HEX);
				break;
                
                case 11:
				_senderId4=aChar;
				_pos++;
                //Serial.print("_senderId4:");
                //Serial.println(_senderId4, HEX);
				break;
                
                default:
                //Serial.print("Data: 0x");
                _pos++;
    //Serial.println(aChar, HEX);
                }
                
                
  }
  if (_pos != 0)
  {
  

  //prettyPrint();
  }
  _pos=0;
}
