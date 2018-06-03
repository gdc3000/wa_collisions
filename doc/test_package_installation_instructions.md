## Testing Instructions of wa_collisions

1. Create a new environment 
    conda create -n wa_collisions_6.0 python=3.6

2. Activate the new environment 
    source activate wa_collisions_6.0

3. Clone the github repository 
    git clone https://github.com/gdc3000/wa_collisions.git

4. Install the package 

    To install the package run the following:
        python setup.py install
    Then install the required dependancies:
        pip install -r requirements.txt
    Install the [Causal Impact](https://github.com/jamalsenouci/causalimpact) package which is not available on pip. 
        pip install git+http://github.com/jamalsenouci/causalimpact.git

5. Check the unittests 
    python -m unittest

6. Confirm that the [jupyter notebook examples](wa_collisions/examples) work 
