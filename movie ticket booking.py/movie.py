from collections import deque

class Movie:
    def __init__(self, movie_id, title, duration):
        self.movie_id = movie_id
        self.title = title
        self.duration = duration

class Theater:
    def __init__(self, theater_id, name, address):
        self.theater_id = theater_id
        self.name = name
        self.address = address

class Screen:
    def __init__(self, screen_id, theater, screen_number, capacity):
        self.screen_id = screen_id
        self.theater = theater
        self.screen_number = screen_number
        self.capacity = capacity
        self.booked_seats = 0

class Ticket:
    def __init__(self, ticket_id, movie, screen, seat_number):
        self.ticket_id = ticket_id
        self.movie = movie
        self.screen = screen
        self.seat_number = seat_number

class BookingSystem:
    def __init__(self):
        self.movies = {}
        self.theaters = {}
        self.screens = {}
        self.tickets = {}
        self.booking_requests = deque()
        self.ticket_counter = 1

    # CRUD operations for movies
    def add_movie(self, movie_id, title, duration):
        self.movies[movie_id] = Movie(movie_id, title, duration)
    
    def view_movie(self, movie_id):
        return self.movies.get(movie_id)
    
    def update_movie(self, movie_id, title=None, duration=None):
        movie = self.movies.get(movie_id)
        if movie:
            if title:
                movie.title = title
            if duration:
                movie.duration = duration
    
    def delete_movie(self, movie_id):
        if movie_id in self.movies:
            del self.movies[movie_id]

    # CRUD operations for theaters
    def add_theater(self, theater_id, name, address):
        self.theaters[theater_id] = Theater(theater_id, name, address)
    
    def view_theater(self, theater_id):
        return self.theaters.get(theater_id)
    
    def update_theater(self, theater_id, name=None, address=None):
        theater = self.theaters.get(theater_id)
        if theater:
            if name:
                theater.name = name
            if address:
                theater.address = address
    
    def delete_theater(self, theater_id):
        if theater_id in self.theaters:
            del self.theaters[theater_id]

    # CRUD operations for screens
    def add_screen(self, screen_id, theater_id, screen_number, capacity):
        theater = self.theaters.get(theater_id)
        if theater:
            self.screens[screen_id] = Screen(screen_id, theater, screen_number, capacity)
    
    def view_screen(self, screen_id):
        return self.screens.get(screen_id)
    
    def update_screen(self, screen_id, screen_number=None, capacity=None):
        screen = self.screens.get(screen_id)
        if screen:
            if screen_number:
                screen.screen_number = screen_number
            if capacity:
                screen.capacity = capacity
    
    def delete_screen(self, screen_id):
        if screen_id in self.screens:
            del self.screens[screen_id]

    # Booking operations
    def book_ticket(self, movie_id, screen_id):
        movie = self.movies.get(movie_id)
        screen = self.screens.get(screen_id)
        if movie and screen and screen.booked_seats < screen.capacity:
            seat_number = screen.booked_seats + 1
            ticket_id = self.ticket_counter
            self.tickets[ticket_id] = Ticket(ticket_id, movie, screen, seat_number)
            screen.booked_seats += 1
            self.ticket_counter += 1
            return ticket_id
        else:
            self.booking_requests.append((movie_id, screen_id))
            return None
    
    def view_ticket(self, ticket_id):
        return self.tickets.get(ticket_id)
    
    def update_ticket(self, ticket_id, movie_id=None, screen_id=None):
        ticket = self.tickets.get(ticket_id)
        if ticket:
            if movie_id:
                movie = self.movies.get(movie_id)
                if movie:
                    ticket.movie = movie
            if screen_id:
                screen = self.screens.get(screen_id)
                if screen and screen.booked_seats < screen.capacity:
                    ticket.screen.booked_seats -= 1
                    ticket.screen = screen
                    ticket.seat_number = screen.booked_seats + 1
                    screen.booked_seats += 1
    
    def cancel_ticket(self, ticket_id):
        ticket = self.tickets.get(ticket_id)
        if ticket:
            ticket.screen.booked_seats -= 1
            del self.tickets[ticket_id]
    
    def view_all_tickets(self):
        return list(self.tickets.values())

# Interactive CLI for the booking system
def main():
    system = BookingSystem()
    
    while True:
        print("\nMovie Ticket Booking System")
        print("1. Add Movie")
        print("2. Add Theater")
        print("3. Add Screen")
        print("4. Book Ticket")
        print("5. View All Tickets")
        print("6. Update Booking")
        print("7. Cancel Booking")
        print("8. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            movie_id = int(input("Enter Movie ID: "))
            title = input("Enter Movie Title: ")
            duration = int(input("Enter Movie Duration: "))
            system.add_movie(movie_id, title, duration)
            print("Movie added successfully.")
        
        elif choice == 2:
            theater_id = int(input("Enter Theater ID: "))
            name = input("Enter Theater Name: ")
            address = input("Enter Theater Address: ")
            system.add_theater(theater_id, name, address)
            print("Theater added successfully.")
        
        elif choice == 3:
            screen_id = int(input("Enter Screen ID: "))
            theater_id = int(input("Enter Theater ID: "))
            screen_number = input("Enter Screen Number: ")
            capacity = int(input("Enter Screen Capacity: "))
            system.add_screen(screen_id, theater_id, screen_number, capacity)
            print("Screen added successfully.")
        
        elif choice == 4:
            movie_id = int(input("Enter Movie ID: "))
            screen_id = int(input("Enter Screen ID: "))
            ticket_id = system.book_ticket(movie_id, screen_id)
            if ticket_id:
                print(f"Ticket booked successfully. Ticket ID: {ticket_id}")
            else:
                print("Booking failed. Added to the waiting list.")
        
        elif choice == 5:
            tickets = system.view_all_tickets()
            if tickets:
                for ticket in tickets:
                    print(f"Ticket ID: {ticket.ticket_id}, Movie: {ticket.movie.title}, Screen: {ticket.screen.screen_number}, Seat Number: {ticket.seat_number}")
            else:
                print("No tickets booked yet.")
        
        elif choice == 6:
            ticket_id = int(input("Enter Ticket ID to update: "))
            movie_id = int(input("Enter new Movie ID (or 0 to skip): "))
            screen_id = int(input("Enter new Screen ID (or 0 to skip): "))
            if movie_id == 0:
                movie_id = None
            if screen_id == 0:
                screen_id = None
            system.update_ticket(ticket_id, movie_id, screen_id)
            print("Booking updated successfully.")
        
        elif choice == 7:
            ticket_id = int(input("Enter Ticket ID to cancel: "))
            system.cancel_ticket(ticket_id)
            print("Booking cancelled successfully.")
        
        elif choice == 8:
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
