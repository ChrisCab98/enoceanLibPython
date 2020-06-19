/*
  EnOceanMsg.h - Library for flashing EnOceanMsg code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/
#ifndef EnOceanMsg_h
#define EnOceanMsg_h

#include "Arduino.h"

#define START_BYTE 0x55

class EnOceanMsg
{
  public:
    EnOceanMsg();
    void decode();
	void reset();
	bool dataAvailable();
    void prettyPrint();
    uint16_t getPacketLength();
    int getPayload();
    uint32_t getSenderId();

  private:
  uint8_t _pos;
  uint8_t _dataLength1;
  uint8_t _dataLength2;
  int _optLength;
  int _packetType;
  int _headerCrc8;
  int _senderId1;
  int _org;
  int _payload;
  int _senderId2;
  int _senderId3;
  int _senderId4;
  
  bool _dataReceived;
};

#endif