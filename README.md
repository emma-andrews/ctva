# Constant Time Vulnerability Analyzer

## Requirements
Python 3.8 or greater. This was tested using Python 3.8.5.

You will need the following packages:
```
pip install networkx
pip install matplotlib
```

Networkx is used to construct and plot networks, which I am using as graph functionality.

Matplotlib allows for the displaying and saving of the resulting graph from Networkx.

```make install``` will install these packages if your Python distribution does not have them.

## How to Run
```python3 main.py``` or ```make```

```config.py``` needs to be in the same directory as ```main.py```. Please edit the sample `config.py` with your values.

## Verilog Samples
This project comes with several working Verilog samples of varying complexity.
If you wish to use your own Verilog sample, please make sure that it can compile with a standard compiler such as Modelsim (now Questasim) or IVerilog and use standard coding conventions.

## HDL FSMs
There are two ways to create an FSM in a hardware description language (HDL): Moore and Mealy. Due to the complexity of Mealy designs with ensuring delay-free output, this tool will only consider Moore designs. A majority of designs are written in Moore due to its simplicity unless otherwise required.

## Why make your own FSM extractor?
While Modelsim and Yosys both have their own FSM extractors, each are very limited in getting that data to be used externally. Modelsim will only graph the FSM for you and can only export the transitions and states as an image. Yosys's extraction would not work, even for the simplest designs and after much researching and debugging. At this point, I felt like I had enough knowledge from trying to get Yosys to work that I was able to write my own parser that will work for simple to medium complexity designs.

## References and Related Documentation
- networkx documentation: https://networkx.org/documentation/stable/
- yosys: https://github.com/YosysHQ/yosys