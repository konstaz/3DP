from decimal import Decimal


DEFAULT_NUMBER_OF_DECIMALS = 3
START_POSITION = [0, 0, 0]


def get_limit_number_of_decimals(number_of_decimals):
    return Decimal('1.{}'.format('0' * number_of_decimals))


def set_to_decimal(value, number_of_decimals):
    number_of_decimals = get_limit_number_of_decimals(number_of_decimals)

    return Decimal(value).quantize(number_of_decimals)


class RotationType:
    RT_XYZ = 0
    RT_YXZ = 1
    RT_YZX = 2
    RT_ZYX = 3
    RT_ZXY = 4
    RT_XZY = 5

    ALL = [RT_XYZ, RT_YXZ, RT_YZX, RT_ZYX, RT_ZXY, RT_XZY]


class Axis:
    sizeX = 0
    sizeY = 1
    sizeZ = 2

    ALL = [sizeX, sizeY, sizeZ]


def rect_intersect(order1, order2, x, y):
    d1 = order1.get_dimension()
    d2 = order2.get_dimension()

    cx1 = order1.position[x] + d1[x]/2
    cy1 = order1.position[y] + d1[y]/2
    cx2 = order2.position[x] + d2[x]/2
    cy2 = order2.position[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def intersect(order1, order2):
    return (
        rect_intersect(order1, order2, Axis.sizeX, Axis.sizeY) and
        rect_intersect(order1, order2, Axis.sizeY, Axis.sizeZ) and
        rect_intersect(order1, order2, Axis.sizeX, Axis.sizeZ)
    )


class Case:
    def __init__(self, id, sizeX, sizeY, sizeZ):
        self.id = id
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeZ = sizeZ
        self.rotation_type = 0
        self.position = START_POSITION
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS


    def format_numbers(self, number_of_decimals):
        self.sizeX = set_to_decimal(self.sizeX, number_of_decimals)
        self.sizeY = set_to_decimal(self.sizeY, number_of_decimals)
        self.sizeZ = set_to_decimal(self.sizeZ, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def string(self):
        return "%s(%sx%sx%s) pos(%s) rt(%s) vol(%s)" % (
            self.id, self.sizeX, self.sizeY, self.sizeZ, self.position, self.rotation_type, self.get_volume()
        )

    def get_volume(self):
        return set_to_decimal(
            self.sizeX * self.sizeY * self.sizeZ, self.number_of_decimals
        )

    def get_dimension(self):
        if self.rotation_type == RotationType.RT_XYZ:
            dimension = [self.sizeX, self.sizeY, self.sizeZ]
        elif self.rotation_type == RotationType.RT_YXZ:
            dimension = [self.sizeY, self.sizeX, self.sizeZ]
        elif self.rotation_type == RotationType.RT_YZX:
            dimension = [self.sizeY, self.sizeZ, self.sizeX]
        elif self.rotation_type == RotationType.RT_ZYX:
            dimension = [self.sizeZ, self.sizeY, self.sizeX]
        elif self.rotation_type == RotationType.RT_ZXY:
            dimension = [self.sizeZ, self.sizeX, self.sizeY]
        elif self.rotation_type == RotationType.RT_XZY:
            dimension = [self.sizeX, self.sizeZ, self.sizeY]
        else:
            dimension = []

        return dimension


class Order:
    def __init__(self, id, sizeX, sizeY, sizeZ):
        self.id = id
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeZ = sizeZ
        self.items = []
        self.unfitted_items = []
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS


    def format_numbers(self, number_of_decimals):
        self.sizeX = set_to_decimal(self.sizeX, number_of_decimals)
        self.sizeY = set_to_decimal(self.sizeY, number_of_decimals)
        self.sizeZ = set_to_decimal(self.sizeZ, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def string(self):
        return "%s(%sx%sx%s) vol(%s)" % (
            self.id, self.sizeX, self.sizeY, self.sizeZ, self.get_volume()
        )

    def get_volume(self):
        return set_to_decimal(
            self.sizeX * self.sizeY * self.sizeZ, self.number_of_decimals
        )

    def put_item(self, item, pivot):
        fit = False
        valid_item_position = item.position
        item.position = pivot

        for i in range(0, len(RotationType.ALL)):
            item.rotation_type = i
            dimension = item.get_dimension()
            if (
                self.sizeX < pivot[0] + dimension[0] or
                self.sizeY < pivot[1] + dimension[1] or
                self.sizeZ < pivot[2] + dimension[2]
            ):
                continue

            fit = True

            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break

            if fit:
                self.items.append(item)

            if not fit:
                item.position = valid_item_position

            return fit

        if not fit:
            item.position = valid_item_position

        return fit


class Packer:
    def __init__(self):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0

    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.itdems.append(item)

    def pack_to_bin(self, bin, item):
        fitted = False

        if not bin.items:
            response = bin.put_item(item, START_POSITION)

            if not response:
                bin.unfitted_items.append(item)

            return

        for axis in range(0, 3):
            items_in_bin = bin.items

            for ib in items_in_bin:
                pivot = [0, 0, 0]
                x, y, z = ib.get_dimension()
                if axis == Axis.sizeX:
                    pivot = [
                        ib.position[0] + x,
                        ib.position[1],
                        ib.position[2]
                    ]
                elif axis == Axis.sizeY:
                    pivot = [
                        ib.position[0],
                        ib.position[1] + y,
                        ib.position[2]
                    ]
                elif axis == Axis.sizeZ:
                    pivot = [
                        ib.position[0],
                        ib.position[1],
                        ib.position[2] + z
                    ]

                if bin.put_item(item, pivot):
                    fitted = True
                    break
            if fitted:
                break

        if not fitted:
            bin.unfitted_items.append(item)

    def pack(
        self, bigger_first=False, distribute_items=False,
        number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS
    ):
        for bin in self.bins:
            bin.format_numbers(number_of_decimals)

        for item in self.items:
            item.format_numbers(number_of_decimals)

        self.bins.sort(
            key=lambda bin: bin.get_volume(), reverse=bigger_first
        )
        self.items.sort(
            key=lambda item: item.get_volume(), reverse=bigger_first
        )

        for bin in self.bins:
            for item in self.items:
                self.pack_to_bin(bin, item)

            if distribute_items:
                for item in bin.items:
                    self.items.remove(item)
