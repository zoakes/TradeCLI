import fire


def test_arguments(input='test.csv',name='zo'):
    print('Test: ', input, name)


# requires fire.Fire(test_arguments)
# PS C:\Users\zach\PycharmProjects\CLI> python fire_args.py --input="testing.csv" --name="ZO"
# Test:  testing.csv ZO

# PRINT out the arguments / types...
#fire.Fire(lambda obj: type(obj).__name__)

# USE arguments (see function, as these are defaulted (optional)
fire.Fire(test_arguments)