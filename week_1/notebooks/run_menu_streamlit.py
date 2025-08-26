"""
Restaurant Menu Management System - Streamlit Version
Run with: streamlit run run_menu_streamlit.py
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Restaurant Menu Manager",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = {
        'Appetizers': [],
        'Main Courses': [],
        'Desserts': [],
        'Beverages': [],
        'Specials': []
    }

if 'restaurant_name' not in st.session_state:
    st.session_state.restaurant_name = "My Restaurant"

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'daily_revenue' not in st.session_state:
    st.session_state.daily_revenue = 0.0

# Constants
DIETARY_OPTIONS = ['🥗 Vegetarian', '🌱 Vegan', '🌾 Gluten-Free', 
                   '🥛 Dairy-Free', '🥜 Nut-Free', '🌶️ Spicy']

# Helper functions
def save_menu_to_file():
    """Save menu to JSON file"""
    data = {
        'restaurant_name': st.session_state.restaurant_name,
        'menu_items': st.session_state.menu_items,
        'last_updated': datetime.now().isoformat()
    }
    with open('streamlit_menu_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    return True

def load_menu_from_file():
    """Load menu from JSON file"""
    if os.path.exists('streamlit_menu_data.json'):
        with open('streamlit_menu_data.json', 'r') as f:
            data = json.load(f)
        st.session_state.menu_items = data['menu_items']
        st.session_state.restaurant_name = data['restaurant_name']
        return True
    return False

def calculate_statistics():
    """Calculate menu statistics"""
    total_items = sum(len(items) for items in st.session_state.menu_items.values())
    
    stats = {
        'Total Items': total_items,
        'Categories': len([cat for cat, items in st.session_state.menu_items.items() if items]),
    }
    
    if total_items > 0:
        all_prices = []
        for items in st.session_state.menu_items.values():
            for item in items:
                all_prices.append(item['price'])
        
        stats['Average Price'] = f"${sum(all_prices)/len(all_prices):.2f}"
        stats['Lowest Price'] = f"${min(all_prices):.2f}"
        stats['Highest Price'] = f"${max(all_prices):.2f}"
    
    return stats

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .category-header {
        font-size: 1.5rem;
        color: #4ECDC4;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .menu-item {
        background-color: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
    }
    .price-tag {
        background-color: #28a745;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🍽️ Restaurant Settings")
    
    # Restaurant name
    new_name = st.text_input("Restaurant Name", st.session_state.restaurant_name)
    if new_name != st.session_state.restaurant_name:
        st.session_state.restaurant_name = new_name
    
    st.markdown("---")
    
    # Navigation
    st.markdown("## 📍 Navigation")
    page = st.radio(
        "Choose a page:",
        ["📋 View Menu", "➕ Add Item", "📊 Statistics", "🛎️ Take Order", "💾 Save/Load"]
    )
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("## 📊 Quick Stats")
    stats = calculate_statistics()
    for key, value in stats.items():
        st.metric(key, value)
    
    st.markdown("---")
    st.markdown("### Today's Performance")
    st.metric("Orders", len(st.session_state.orders))
    st.metric("Revenue", f"${st.session_state.daily_revenue:.2f}")

# Main content area
st.markdown(f'<h1 class="main-header">{st.session_state.restaurant_name}</h1>', unsafe_allow_html=True)

# Page routing
if page == "📋 View Menu":
    st.markdown("## 📋 Full Menu")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + list(st.session_state.menu_items.keys())
        )
    with col2:
        price_filter = st.slider(
            "Max Price",
            0, 100, 100,
            format="$%d"
        )
    with col3:
        dietary_filter = st.multiselect(
            "Dietary Restrictions",
            DIETARY_OPTIONS
        )
    
    # Display menu
    categories_to_show = (st.session_state.menu_items.keys() 
                         if category_filter == "All" 
                         else [category_filter])
    
    for category in categories_to_show:
        items = st.session_state.menu_items[category]
        if items:
            st.markdown(f'<div class="category-header">🍴 {category}</div>', unsafe_allow_html=True)
            
            # Create columns for grid layout
            cols = st.columns(2)
            for idx, item in enumerate(items):
                # Apply filters
                if item['price'] > price_filter:
                    continue
                if dietary_filter and not any(d in item.get('dietary', []) for d in dietary_filter):
                    continue
                
                with cols[idx % 2]:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"### {item['name']}")
                            if item.get('description'):
                                st.markdown(f"*{item['description']}*")
                            if item.get('dietary'):
                                st.markdown(" ".join(item['dietary']))
                            if item.get('rating', 0) > 0:
                                stars = "⭐" * int(item['rating'])
                                st.markdown(f"{stars} ({item['rating']:.1f}/5)")
                        with col2:
                            st.markdown(f"### ${item['price']:.2f}")
                            if st.button("🗑️", key=f"del_{category}_{idx}"):
                                items.pop(idx)
                                st.rerun()
                        st.markdown("---")

elif page == "➕ Add Item":
    st.markdown("## ➕ Add New Menu Item")
    
    with st.form("add_item_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Dish Name *", placeholder="e.g., Caesar Salad")
            category = st.selectbox("Category *", list(st.session_state.menu_items.keys()))
            price = st.number_input("Price ($) *", min_value=0.01, value=10.00, step=0.01)
        
        with col2:
            description = st.text_area("Description", placeholder="Delicious fresh salad with...")
            dietary = st.multiselect("Dietary Information", DIETARY_OPTIONS)
            available = st.checkbox("Available for ordering", value=True)
        
        submitted = st.form_submit_button("➕ Add to Menu", use_container_width=True)
        
        if submitted:
            if name:
                new_item = {
                    'name': name,
                    'price': price,
                    'description': description,
                    'dietary': dietary,
                    'available': available,
                    'rating': 0,
                    'review_count': 0
                }
                st.session_state.menu_items[category].append(new_item)
                st.success(f"✅ '{name}' added to {category}!")
                st.balloons()
            else:
                st.error("Please enter a dish name!")

elif page == "📊 Statistics":
    st.markdown("## 📊 Menu Analytics")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_items = sum(len(items) for items in st.session_state.menu_items.values())
    with col1:
        st.metric("Total Menu Items", total_items)
    with col2:
        active_categories = len([cat for cat, items in st.session_state.menu_items.items() if items])
        st.metric("Active Categories", active_categories)
    with col3:
        st.metric("Today's Orders", len(st.session_state.orders))
    with col4:
        st.metric("Today's Revenue", f"${st.session_state.daily_revenue:.2f}")
    
    # Category breakdown
    st.markdown("### 📊 Items by Category")
    category_data = {cat: len(items) for cat, items in st.session_state.menu_items.items()}
    
    if any(category_data.values()):
        df = pd.DataFrame(list(category_data.items()), columns=['Category', 'Count'])
        st.bar_chart(df.set_index('Category'))
    
    # Price analysis
    st.markdown("### 💰 Price Analysis")
    all_items = []
    for category, items in st.session_state.menu_items.items():
        for item in items:
            all_items.append({
                'Category': category,
                'Item': item['name'],
                'Price': item['price']
            })
    
    if all_items:
        df_items = pd.DataFrame(all_items)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Price Distribution")
            st.bar_chart(df_items.groupby('Category')['Price'].mean())
        
        with col2:
            st.markdown("#### Top 5 Most Expensive Items")
            top_items = df_items.nlargest(5, 'Price')[['Item', 'Price', 'Category']]
            st.dataframe(top_items, hide_index=True)
    
    # Best rated items
    st.markdown("### ⭐ Top Rated Items")
    rated_items = []
    for category, items in st.session_state.menu_items.items():
        for item in items:
            if item.get('review_count', 0) > 0:
                rated_items.append({
                    'Item': item['name'],
                    'Category': category,
                    'Rating': item.get('rating', 0),
                    'Reviews': item.get('review_count', 0)
                })
    
    if rated_items:
        df_rated = pd.DataFrame(rated_items).sort_values('Rating', ascending=False).head(5)
        st.dataframe(df_rated, hide_index=True)
    else:
        st.info("No items have been rated yet.")

elif page == "🛎️ Take Order":
    st.markdown("## 🛎️ Take Customer Order")
    
    # Get available items
    available_items = []
    for category, items in st.session_state.menu_items.items():
        for item in items:
            if item.get('available', True):
                available_items.append(f"[{category}] {item['name']} - ${item['price']:.2f}")
    
    if available_items:
        # Order form
        with st.form("order_form"):
            st.markdown("### Select Items")
            
            selected_items = st.multiselect(
                "Choose items for the order:",
                available_items
            )
            
            quantities = {}
            if selected_items:
                st.markdown("### Specify Quantities")
                cols = st.columns(2)
                for idx, item_str in enumerate(selected_items):
                    with cols[idx % 2]:
                        quantities[item_str] = st.number_input(
                            f"{item_str.split('] ')[1].split(' - ')[0]}",
                            min_value=1, value=1, key=f"qty_{idx}"
                        )
            
            customer_name = st.text_input("Customer Name (optional)")
            notes = st.text_area("Order Notes (optional)")
            
            submitted = st.form_submit_button("📝 Place Order", use_container_width=True)
            
            if submitted and selected_items:
                # Calculate total
                order_total = 0
                order_details = []
                
                for item_str, qty in quantities.items():
                    # Extract price from string
                    price_str = item_str.split('$')[1]
                    price = float(price_str)
                    item_total = price * qty
                    order_total += item_total
                    
                    order_details.append({
                        'item': item_str.split('] ')[1].split(' - ')[0],
                        'quantity': qty,
                        'price': price,
                        'total': item_total
                    })
                
                # Add to session state
                st.session_state.orders.append({
                    'timestamp': datetime.now(),
                    'customer': customer_name or "Guest",
                    'items': order_details,
                    'total': order_total,
                    'notes': notes
                })
                st.session_state.daily_revenue += order_total
                
                # Show receipt
                st.success("✅ Order placed successfully!")
                st.markdown("### 🧾 Receipt")
                st.markdown(f"**Customer:** {customer_name or 'Guest'}")
                st.markdown(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
                
                for detail in order_details:
                    st.markdown(f"- {detail['quantity']}x {detail['item']}: ${detail['total']:.2f}")
                
                st.markdown(f"### **Total: ${order_total:.2f}**")
                st.balloons()
    else:
        st.warning("No items available for ordering. Please add items to the menu first!")

elif page == "💾 Save/Load":
    st.markdown("## 💾 Save/Load Menu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💾 Save Menu")
        st.markdown("Save your current menu to a file")
        
        if st.button("💾 Save Current Menu", use_container_width=True):
            if save_menu_to_file():
                st.success("✅ Menu saved successfully!")
        
        # Export as JSON
        st.markdown("### 📥 Download Menu")
        menu_data = {
            'restaurant_name': st.session_state.restaurant_name,
            'menu_items': st.session_state.menu_items,
            'exported_at': datetime.now().isoformat()
        }
        json_str = json.dumps(menu_data, indent=2)
        
        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name=f"{st.session_state.restaurant_name.replace(' ', '_')}_menu.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        st.markdown("### 📂 Load Menu")
        st.markdown("Load a previously saved menu")
        
        if st.button("📂 Load Saved Menu", use_container_width=True):
            if load_menu_from_file():
                st.success("✅ Menu loaded successfully!")
                st.rerun()
            else:
                st.error("No saved menu found!")
        
        # Upload JSON
        st.markdown("### 📤 Upload Menu")
        uploaded_file = st.file_uploader("Choose a JSON file", type=['json'])
        
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                st.session_state.menu_items = data.get('menu_items', {})
                st.session_state.restaurant_name = data.get('restaurant_name', 'My Restaurant')
                st.success("✅ Menu uploaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {e}")

# Footer
st.markdown("---")
st.markdown(
    f"<center>🍽️ {st.session_state.restaurant_name} Menu System | "
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</center>",
    unsafe_allow_html=True
)