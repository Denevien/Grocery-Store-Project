"""Assignment 1 - Grocery Store Events (Task 2)

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
# Feel free to import classes and functions from
# *your other files*, but remember not to import any external libraries.
from store import *


class Event:
    """An event.

    Events have an ordering based on the event timestamp in non-ascending
    order. Events with older timestamps are less than those with newer
    timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = int(timestamp)

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return whether this Event is equal to <other>.

        Two events are equal if they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self.__le__(other)

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self.__lt__(other)

    def do(self, store):
        """Perform this Event.

        Call methods on <store> to update its state according to the
        meaning of the event. Note: the "business logic" of what actually
        happens inside a grocery store should be handled in the GroceryStore
        class, not in any Event classes.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        @type self: Event
        @type store: GroceryStore
        @rtype: list[Event]
            A list of events generated by performing this event.
        """
        raise NotImplementedError


# TODO: Create subclasses for the different types of events below.

class BeginCheckout(Event):
    # creating a begin checkout event to return to the simulation

    def __init__(self, new_timestamp, customer):
        super().__init__(new_timestamp)
        self.customer = customer

    def __repr__(self):
        # string representation of the begin checkout function
        # 'Timestamp:60 , Cust_id: BOb , Prod Count: 12'

        return str(self.timestamp) + " " + str(
            self.customer.cust_id) + " " + str(
            self.customer.num_items) + " BC"

    def do(self, store):
        """ takes the customer object and determines the checkoutline occupied
        to calculate a new checkout time for the finish checkout object to be
        returned
        @type self : BeginCheckout Object
        @type store: GroceryStore Object
        @rtype: list[Event]
        """

        # determine which checkoutline is being occupied by the customer
        checkout_line = store.customer_checkout_line(self.customer)
        # takes original timestamp argument and modifys it based
        # on checkoutline type
        new_timestamp = checkout_line.checkout_time(self.timestamp,
                                                    self.customer)
        return [FinishCheckout(new_timestamp, self.customer)]


class FinishCheckout(Event):
    """ Once the customer has reached the end of the"""

    def __init__(self, new_timestamp, customer):
        super().__init__(new_timestamp)
        self.customer = customer

    def __repr__(self):
        """returns a string representation of the customer object
        which can be used to construct the object again
        # 'Timestamp:60 , Cust_id: BOb , PRod Count: 12' """

        return str(self.timestamp) + " " + str(
            self.customer.cust_id) + " " + str(
            self.customer.num_items) + " " + str('FC')


    def do(self, store):
        """ This creates  and assigns the current timestamp
        to a begin checkout event and returns the event in a list
        @type self: FinishCheckout Object
        @type store: GroceryStore Object
        @rtype: List[Events]
        """
        #return a customer object that is next to be processed
        next_customer = store.next_customer_in_line(self.customer)
        #print('Next Customer'next_customer)
        if next_customer is None:
            #print(' successful none customer')
            event_list = []
        else:
            # the next customer in the line  gets a "begin checking out" event
            # with the same timestamp as the "finish" event
            event_list = [BeginCheckout(self.timestamp, next_customer)]

        return event_list


class CustomerArrive(Event):
    """Once the customer info is read from the file the second element
    is confirmed as 'Arrive'
    """

    def __init__(self, timestamp, cust_id, num_items):
        super().__init__(timestamp)

        self.cust_id = cust_id
        self.num_items = num_items

    def __repr__(self):
        # returns a string representation of the customer object which
        # can be used to construct the object again
        # 'Timestamp:60 , Cust_id: BOb , PRod Count: 12'

        return str(self.timestamp) + " " + str(self.cust_id) + " " + str(
            self.num_items) + " " + str('CA')


    def do(self, store):
        """Returns an list of events generated after accepting the initial event"""
        new_events_list = []

        customer = store.new_customer(self.cust_id, self.num_items)
        cust_pos_in_line = store.customer_position(customer)
        # if the customer is at the front of the line join line,begin checkout
        if cust_pos_in_line == 0:
            #add these two generated events to our list of events to pass
            print('Cx evaluated as front of the line')
            new_events_list.append(BeginCheckout(self.timestamp, customer))
            #new_events_list.append(FinishCheckout(self.timestamp, customer))

        return new_events_list

class ChangeLine(Event):
    """ This takes the customers from the recently closed checkoutline and finds
    a new OPEN line to place the customer in
    """
    def __init__(self, timestamp, customer):
        super().__init__(timestamp)
        self.customer = customer

    def __repr__(self):
        pass

    def do(self, store):
        """this takes the customer object and reassigns it to a new
        checkoutline """

        new_events_list = []
        #establishes the shortest line available for the moving customer
        shortest_line = store.shortest_open_line()
        #appends the customer to the shortest line available
        shortest_line.cust_in_line_list.append(self.customer)
        cust_pos_in_line = store.customer_position(self.customer)
        # if the customer is at the front of the line join line,begin checkout
        if cust_pos_in_line == 0:
            #add these two generated events to our list of events to pass
            new_events_list.append(BeginCheckout(self.timestamp, self.customer))



        return new_events_list


class LineClose(Event):
    """Once the checkout counter information is updated as 'Close' all customers
    except the next in line.All subsequent customers in line become
    CustomerArrive events as
    now have to rejoin available checkoutlines"""


    def __init__(self, timestamp, closing_checkout_number):
        super().__init__(timestamp)
        self.closing_checkout_number = closing_checkout_number

    def __repr__(self):
        # returns a string representation of the object which can be used to construct the object again
        # 'Timestamp:5 , 'Close' , Closing_checkout_number: 2'

        return str(self.timestamp) + " " + (self.closing_checkout_number) + " LC"

    def do(self, store):
        """ If a line closes, there is one new "customer joins" event per
        customer in the checkout line after the first one. The new events
        should be spaced 1 second apart, with the last customer in the line
        having the earliest "new customer" event, which is the same as the
        "line close" event
        @type self: LineClose object
        @type store: GroceryStore object
        @rtype: List[Customers]
        """

        events_list = []
        for customer in store.empty_customers_in_line(int(self.closing_checkout_number)):
            events_list.append(ChangeLine(self.timestamp, customer))

        return events_list


# TODO: Complete this function, which creates a list of events from a file.
def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """
    events = []
    with open(filename, 'r') as file:

        for line in file:

            # Create a list of words in the line, e.g.
            # ['60', 'Arrive', 'Bob', '5'].
            # Note that these are strings, and you'll need to convert some of
            # them to ints.
            # in our example, token[0] ='60'
            tokens = line.split()

            if 'Arrive' == tokens[1]:
                # create arrival event and append it to events list
                # creating a customer arrival event
                # tokens[0] = timestamp
                # tokens[1] =  type of event
                # tokens[2] =cust_id
                # tokens[3] =  number of items in customer  basket

                events.append(CustomerArrive(tokens[0], tokens[2], tokens[3]))

            elif 'Close' == tokens[1]:
                # create checkoutlane closure event and add it to the events list

                events.append(LineClose(tokens[0], tokens[2]))
            else:
                # to account for any illogical events read
                raise NotImplementedError

    return events


if __name__ == '__main__':
    import doctest

    doctest.testmod()
