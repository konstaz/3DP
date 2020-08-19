Before you start using the algorithm it is necessary to type certain commands in the terminal:

- python3 -m venv env
- . env/bin/activate
- pip install -r requirements.txt

Use:

    from main import *

    packer = Packer()
    packer.add_bin(Order(11.5, 6.125, 0.25, 10))
    packer.add_bin(Order(15.0, 12.0, 0.75, 15))
    packer.add_bin(Order(8.625, 5.375, 1.625, 70.0))
    packer.add_bin(Order(11.0, 8.5, 5.5, 70.0))
    packer.add_bin(Order(13.625, 11.875, 3.375, 70.0))
    packer.add_bin(Order(12.0, 12.0, 5.5, 70.0))
    packer.add_bin(Order(23.6875, 11.75, 3.0, 70.0))

    packer.add_item(Case(3.9370, 1.9685, 1.9685, 1))
    packer.add_item(Case(3.9370, 1.9685, 1.9685, 2))
    packer.add_item(Case(3.9370, 1.9685, 1.9685, 3))
    packer.add_item(Case(7.8740, 3.9370, 1.9685, 4))
    packer.add_item(Case(7.8740, 3.9370, 1.9685, 5))
    packer.add_item(Case(7.8740, 3.9370, 1.9685, 6))
    packer.add_item(Case(7.8740, 3.9370, 1.9685, 7))
    packer.add_item(Case(7.8740, 3.9370, 1.9685, 8))
    packer.add_item(Case(7.8740, 3.9370, 1.9685, 9))

    packer.pack()

    for b in packer.bins:
        print(":", b.string())

        print("FITTED ITEMS:")
        for item in b.items:
            print("> ", item.string())

        print("UNFITTED ITEMS:")
        for item in b.unfitted_items:
            print("> ", item.string())
