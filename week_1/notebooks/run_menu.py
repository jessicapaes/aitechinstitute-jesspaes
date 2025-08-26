#!/usr/bin/env python3
"""
Restaurant Menu Management System
A complete interactive restaurant menu application
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class MenuItem:
    """Represents a single menu item"""
    def __init__(self, name: str, price: float, category: str, description: str = "", 
                 dietary_info: List[str] = None, is_available: bool = True):
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.dietary_info = dietary_info or []
        self.is_available = is_available
        self.rating = 0.0
        self.review_count = 0
    
    def to_dict(self) -> dict:
        """Convert MenuItem to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'description': self.description,
            'dietary_info': self.dietary_info,
            'is_available': self.is_available,
            'rating': self.rating,
            'review_count': self.review_count
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create MenuItem from dictionary"""
        item = cls(
            name=data['name'],
            price=data['price'],
            category=data['category'],
            description=data.get('description', ''),
            dietary_info=data.get('dietary_info', []),
            is_available=data.get('is_available', True)
        )
        item.rating = data.get('rating', 0.0)
        item.review_count = data.get('review_count', 0)
        return item
    
    def display(self) -> str:
        """Display formatted menu item"""
        availability = "✓" if self.is_available else "✗"
        dietary = f" ({', '.join(self.dietary_info)})" if self.dietary_info else ""
        rating_stars = "⭐" * int(self.rating) if self.rating > 0 else "No ratings"
        
        display_str = f"\n  [{availability}] {self.name}{dietary} - ${self.price:.2f}"
        if self.description:
            display_str += f"\n      {self.description}"
        if self.review_count > 0:
            display_str += f"\n      Rating: {rating_stars} ({self.rating:.1f}/5 from {self.review_count} reviews)"
        return display_str


class RestaurantMenu:
    """Main restaurant menu management system"""
    
    CATEGORIES = ['Appetizers', 'Main Courses', 'Desserts', 'Beverages', 'Specials']
    DIETARY_OPTIONS = ['Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Spicy']
    
    def __init__(self, restaurant_name: str = "My Restaurant"):
        self.restaurant_name = restaurant_name
        self.menu_items: Dict[str, List[MenuItem]] = {category: [] for category in self.CATEGORIES}
        self.currency = "$"
        self.orders_today = []
        self.daily_revenue = 0.0
        
    def save_menu(self, filename: str = "menu_data.json"):
        """Save menu to JSON file"""
        data = {
            'restaurant_name': self.restaurant_name,
            'menu_items': {},
            'currency': self.currency,
            'last_updated': datetime.now().isoformat()
        }
        
        for category, items in self.menu_items.items():
            data['menu_items'][category] = [item.to_dict() for item in items]
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Menu saved to {filename}")
    
    def load_menu(self, filename: str = "menu_data.json"):
        """Load menu from JSON file"""
        if not os.path.exists(filename):
            print(f"No saved menu found at {filename}")
            return False
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.restaurant_name = data['restaurant_name']
        self.currency = data.get('currency', '$')
        
        self.menu_items = {category: [] for category in self.CATEGORIES}
        for category, items_data in data['menu_items'].items():
            if category in self.menu_items:
                self.menu_items[category] = [MenuItem.from_dict(item) for item in items_data]
        
        print(f"✅ Menu loaded from {filename}")
        return True
    
    def add_item(self):
        """Interactive function to add a new menu item"""
        print("\n🍽️  ADD NEW MENU ITEM")
        print("-" * 40)
        
        # Get category
        print("\nSelect category:")
        for i, category in enumerate(self.CATEGORIES, 1):
            print(f"{i}. {category}")
        
        while True:
            try:
                cat_choice = int(input("\nEnter category number: ")) - 1
                if 0 <= cat_choice < len(self.CATEGORIES):
                    category = self.CATEGORIES[cat_choice]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
        
        # Get item details
        name = input("Enter dish name: ").strip()
        
        while True:
            try:
                price = float(input("Enter price: $"))
                if price > 0:
                    break
                else:
                    print("Price must be positive.")
            except ValueError:
                print("Please enter a valid number.")
        
        description = input("Enter description (optional): ").strip()
        
        # Get dietary info
        print("\nSelect dietary information (enter numbers separated by commas, or press Enter to skip):")
        for i, option in enumerate(self.DIETARY_OPTIONS, 1):
            print(f"{i}. {option}")
        
        dietary_input = input("Your choices: ").strip()
        dietary_info = []
        if dietary_input:
            try:
                choices = [int(x.strip()) - 1 for x in dietary_input.split(',')]
                dietary_info = [self.DIETARY_OPTIONS[i] for i in choices if 0 <= i < len(self.DIETARY_OPTIONS)]
            except (ValueError, IndexError):
                print("Invalid dietary choices, skipping...")
        
        # Create and add item
        new_item = MenuItem(name, price, category, description, dietary_info)
        self.menu_items[category].append(new_item)
        
        print(f"\n✅ '{name}' added to {category} successfully!")
        return new_item
    
    def remove_item(self):
        """Remove an item from the menu"""
        print("\n🗑️  REMOVE MENU ITEM")
        print("-" * 40)
        
        # Display all items with numbers
        all_items = []
        for category, items in self.menu_items.items():
            for item in items:
                all_items.append((item, category))
        
        if not all_items:
            print("No items in menu to remove.")
            return
        
        print("\nSelect item to remove:")
        for i, (item, category) in enumerate(all_items, 1):
            print(f"{i}. [{category}] {item.name} - ${item.price:.2f}")
        
        while True:
            try:
                choice = int(input("\nEnter item number (0 to cancel): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(all_items):
                    item_to_remove, category = all_items[choice - 1]
                    self.menu_items[category].remove(item_to_remove)
                    print(f"✅ '{item_to_remove.name}' removed from menu.")
                    return
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
    
    def update_item(self):
        """Update an existing menu item"""
        print("\n✏️  UPDATE MENU ITEM")
        print("-" * 40)
        
        # Display all items
        all_items = []
        for category, items in self.menu_items.items():
            for item in items:
                all_items.append((item, category))
        
        if not all_items:
            print("No items in menu to update.")
            return
        
        print("\nSelect item to update:")
        for i, (item, category) in enumerate(all_items, 1):
            availability = "Available" if item.is_available else "Unavailable"
            print(f"{i}. [{category}] {item.name} - ${item.price:.2f} ({availability})")
        
        while True:
            try:
                choice = int(input("\nEnter item number (0 to cancel): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(all_items):
                    item_to_update, _ = all_items[choice - 1]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
        
        # Update menu
        print(f"\nUpdating: {item_to_update.name}")
        print("1. Update price")
        print("2. Update description")
        print("3. Toggle availability")
        print("4. Update dietary info")
        
        update_choice = input("\nWhat would you like to update? ")
        
        if update_choice == "1":
            try:
                new_price = float(input(f"Enter new price (current: ${item_to_update.price:.2f}): $"))
                item_to_update.price = new_price
                print("✅ Price updated!")
            except ValueError:
                print("Invalid price.")
        elif update_choice == "2":
            new_desc = input(f"Enter new description (current: {item_to_update.description}): ")
            item_to_update.description = new_desc
            print("✅ Description updated!")
        elif update_choice == "3":
            item_to_update.is_available = not item_to_update.is_available
            status = "available" if item_to_update.is_available else "unavailable"
            print(f"✅ Item is now {status}!")
        elif update_choice == "4":
            print(f"Current dietary info: {', '.join(item_to_update.dietary_info) if item_to_update.dietary_info else 'None'}")
            print("\nSelect new dietary information (enter numbers separated by commas):")
            for i, option in enumerate(self.DIETARY_OPTIONS, 1):
                print(f"{i}. {option}")
            dietary_input = input("Your choices: ").strip()
            if dietary_input:
                try:
                    choices = [int(x.strip()) - 1 for x in dietary_input.split(',')]
                    item_to_update.dietary_info = [self.DIETARY_OPTIONS[i] for i in choices if 0 <= i < len(self.DIETARY_OPTIONS)]
                    print("✅ Dietary info updated!")
                except (ValueError, IndexError):
                    print("Invalid choices.")
    
    def display_menu(self):
        """Display the complete menu"""
        print(f"\n{'='*50}")
        print(f"🍴 {self.restaurant_name.upper()} MENU 🍴".center(50))
        print(f"{'='*50}")
        
        if not any(items for items in self.menu_items.values()):
            print("\nMenu is empty. Add some items first!")
            return
        
        for category, items in self.menu_items.items():
            if items:
                print(f"\n📍 {category.upper()}")
                print("-" * 30)
                for item in items:
                    print(item.display())
        
        print(f"\n{'='*50}")
        print(f"All prices in {self.currency}")
        
        # Statistics
        total_items = sum(len(items) for items in self.menu_items.values())
        available_items = sum(1 for items in self.menu_items.values() for item in items if item.is_available)
        print(f"\n📊 Total items: {total_items} | Available: {available_items}")
    
    def search_menu(self):
        """Search for items in the menu"""
        print("\n🔍 SEARCH MENU")
        print("-" * 40)
        
        search_term = input("Enter search term (name or dietary restriction): ").lower()
        found_items = []
        
        for category, items in self.menu_items.items():
            for item in items:
                if (search_term in item.name.lower() or 
                    search_term in item.description.lower() or
                    any(search_term in dietary.lower() for dietary in item.dietary_info)):
                    found_items.append((item, category))
        
        if found_items:
            print(f"\n📋 Found {len(found_items)} item(s):")
            for item, category in found_items:
                print(f"\n[{category}] {item.name} - ${item.price:.2f}")
                if item.description:
                    print(f"  {item.description}")
                if item.dietary_info:
                    print(f"  Dietary: {', '.join(item.dietary_info)}")
        else:
            print(f"No items found matching '{search_term}'")
    
    def take_order(self):
        """Take a customer order"""
        print("\n📝 TAKE ORDER")
        print("-" * 40)
        
        order = []
        order_total = 0.0
        
        while True:
            # Display available items
            available_items = []
            for category, items in self.menu_items.items():
                for item in items:
                    if item.is_available:
                        available_items.append((item, category))
            
            if not available_items:
                print("No items available for ordering.")
                return
            
            print("\nAvailable items:")
            for i, (item, category) in enumerate(available_items, 1):
                dietary = f" ({', '.join(item.dietary_info)})" if item.dietary_info else ""
                print(f"{i}. [{category}] {item.name}{dietary} - ${item.price:.2f}")
            
            try:
                choice = input("\nEnter item number (or 'done' to finish): ").strip()
                if choice.lower() == 'done':
                    break
                
                item_idx = int(choice) - 1
                if 0 <= item_idx < len(available_items):
                    item, _ = available_items[item_idx]
                    
                    quantity = int(input(f"Quantity for {item.name}: "))
                    if quantity > 0:
                        order.append((item, quantity))
                        item_total = item.price * quantity
                        order_total += item_total
                        print(f"✅ Added {quantity}x {item.name} (${item_total:.2f})")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")
        
        if order:
            print("\n" + "="*40)
            print("ORDER SUMMARY")
            print("-"*40)
            for item, qty in order:
                print(f"{qty}x {item.name} - ${item.price * qty:.2f}")
            print("-"*40)
            print(f"TOTAL: ${order_total:.2f}")
            
            confirm = input("\nConfirm order? (y/n): ").lower()
            if confirm == 'y':
                self.orders_today.append(order)
                self.daily_revenue += order_total
                print("✅ Order confirmed!")
                
                # Ask for ratings
                rate = input("Would the customer like to rate any items? (y/n): ").lower()
                if rate == 'y':
                    for item, _ in order:
                        rating = input(f"Rate {item.name} (1-5 stars, or skip): ").strip()
                        if rating and rating.isdigit():
                            rating_val = int(rating)
                            if 1 <= rating_val <= 5:
                                # Update item rating
                                old_total = item.rating * item.review_count
                                item.review_count += 1
                                item.rating = (old_total + rating_val) / item.review_count
                                print(f"✅ Thank you for rating {item.name}!")
    
    def view_statistics(self):
        """View menu and sales statistics"""
        print("\n📊 RESTAURANT STATISTICS")
        print("="*50)
        
        # Menu statistics
        total_items = sum(len(items) for items in self.menu_items.values())
        available_items = sum(1 for items in self.menu_items.values() for item in items if item.is_available)
        
        print(f"\n📋 Menu Statistics:")
        print(f"  Total items: {total_items}")
        print(f"  Available items: {available_items}")
        
        for category, items in self.menu_items.items():
            if items:
                avg_price = sum(item.price for item in items) / len(items)
                print(f"  {category}: {len(items)} items (avg price: ${avg_price:.2f})")
        
        # Find best rated items
        all_items = [(item, cat) for cat, items in self.menu_items.items() for item in items]
        rated_items = [(item, cat) for item, cat in all_items if item.review_count > 0]
        
        if rated_items:
            rated_items.sort(key=lambda x: x[0].rating, reverse=True)
            print(f"\n⭐ Top Rated Items:")
            for item, category in rated_items[:3]:
                print(f"  {item.name} ({category}): {item.rating:.1f}/5 ({item.review_count} reviews)")
        
        # Sales statistics
        print(f"\n💰 Today's Sales:")
        print(f"  Orders: {len(self.orders_today)}")
        print(f"  Revenue: ${self.daily_revenue:.2f}")
        
        if self.orders_today:
            # Most popular items today
            item_counts = {}
            for order in self.orders_today:
                for item, qty in order:
                    if item.name not in item_counts:
                        item_counts[item.name] = 0
                    item_counts[item.name] += qty
            
            popular = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
            print(f"\n🔥 Today's Best Sellers:")
            for name, count in popular[:3]:
                print(f"  {name}: {count} orders")


def main():
    """Main program loop"""
    print("\n" + "="*50)
    print("🍽️  RESTAURANT MENU MANAGEMENT SYSTEM 🍽️".center(50))
    print("="*50)
    
    # Initialize or load restaurant
    restaurant_name = input("\nEnter your restaurant name: ").strip() or "My Restaurant"
    menu = RestaurantMenu(restaurant_name)
    
    # Try to load existing menu
    if os.path.exists("menu_data.json"):
        load = input("\nFound existing menu data. Load it? (y/n): ").lower()
        if load == 'y':
            menu.load_menu()
    
    while True:
        print(f"\n{'='*50}")
        print(f"🏠 {menu.restaurant_name} - Main Menu")
        print("="*50)
        print("\n1. 📝 Add new dish")
        print("2. 🗑️  Remove dish")
        print("3. ✏️  Update dish")
        print("4. 📋 Display full menu")
        print("5. 🔍 Search menu")
        print("6. 🛎️  Take order")
        print("7. 📊 View statistics")
        print("8. 💾 Save menu")
        print("9. 📂 Load menu")
        print("0. 🚪 Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            menu.add_item()
        elif choice == '2':
            menu.remove_item()
        elif choice == '3':
            menu.update_item()
        elif choice == '4':
            menu.display_menu()
        elif choice == '5':
            menu.search_menu()
        elif choice == '6':
            menu.take_order()
        elif choice == '7':
            menu.view_statistics()
        elif choice == '8':
            menu.save_menu()
        elif choice == '9':
            filename = input("Enter filename (default: menu_data.json): ").strip() or "menu_data.json"
            menu.load_menu(filename)
        elif choice == '0':
            save = input("\nSave menu before exiting? (y/n): ").lower()
            if save == 'y':
                menu.save_menu()
            print(f"\nThank you for using {menu.restaurant_name} Menu System!")
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please try again.")
    
    return menu


if __name__ == "__main__":
    menu = main()