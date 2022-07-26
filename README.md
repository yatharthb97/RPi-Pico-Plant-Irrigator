# Raspberry Pi Pico Plant Irrigator

### Microcontroller Used: [RaspberryPi-Pico : RP2040](https://www.raspberrypi.com/products/raspberry-pi-pico/)

<p style="align:centre">
    <img src="https://images.ctfassets.net/2lpsze4g694w/4jQGyUQTjMglSA7GjGvGPa/10949b5cd522330327e7d9917589c1f9/PICO_BOARD_TOP_WHITE.jpg?w=800" width=50%>
</p>



## Read Project Article for Details

Read [here](https://yatharthb97.github.io/projects/auto_irrigation/).

Some basic information is given below.



## Peripheral Connections

```mermaid
flowchart LR;
	
	subgraph "Relay Ch1";
		Pump -.- Mains(("~<br>Mains"))
	end
	
	subgraph "Relay Ch2";
		Buzzer -.- Battery(("9V<br>Battery"))
	end
	
	%% Control Module
	subgraph "⚙️"
		subgraph Relay
			direction LR
			SP(Start Pump) --> Pump
			SB("StartBuzzer") --> Buzzer
			%%SP ---> SB
		end
		Pico-MCU["Pico-MCU"] -."connects to".- Relay
		style Pico-MCU fill:#6acf65,stroke:#333,stroke-width:4px, stroke-dasharray: 5 5
	end
	
	%% Manual Pump Operation using Touch Switch
	subgraph "Maunal Switching"
		TS -. "connects to" .-> Pico-MCU
		TS{"Touch<br>Switch"} --"true"--> SP
		TS--false-->X((X))
		Pico-MCU
	end
```





## Decision Flowchart

```mermaid
flowchart LR
	subgraph "-"
	direction LR
		RTC[("DS1302<br>RTC")] --current_time--> check_time{"current time<br>==<br>watering time"}
		check_time --true--> run_pump
		run_pump["Run Pump(2 min)"] ---> S13("Sleep(13 min)")
		check_time --false--> S15("sleep(15 min)")
		S13 -. return .-> check_time
		S15 -. return .-> check_time
	end
```

## Operations

#### Running Pump Equivalent

```mermaid
flowchart LR;
	RP("Run Pump") --> SP("Start Pump")
	RP --> SB("Start Buzzer")
	SB -.- X["Sound Continuously"]
```

#### Manual Operations

```mermaid
flowchart LR;
	TS{"Touch<br>Switch"} --true-->RP("Run Pump")
	TS--false-->X(("X"))
```

#### Alarm: alert the user for starting manual pump operation

```mermaid
flowchart LR;
	RTC[("DS1302<br>RTC")] --current time --> Q{"curent time<br>==<br>alarm time"}
	Q --true--> RB("Run Buzzer<br>(1 min)")
	RB-.-Sound[Beeping Sound]
```

