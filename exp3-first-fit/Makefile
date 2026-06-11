CXX = g++
CXXFLAGS = -Wall -std=c++11 -O2
TARGET = first_fit

all: $(TARGET)

$(TARGET): first_fit.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) first_fit.cpp

clean:
	rm -f $(TARGET)

.PHONY: all clean
