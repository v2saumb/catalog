from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, User, Items
import datetime

engine = create_engine('sqlite://catalog:catalog@localhost/catalogdb')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# inserting record for admin user
newUser = User(name="Admin", email="admin@itemcatalog.com", accounttype="ADMIN",
               lastlogin=datetime.date.today(), password="123456")
try:
    existinguser = session.query(User).filter(
        User.email == newUser.email).one()
except:
    existinguser = None
if existinguser is None:
    print "Creating User "
    session.add(newUser)
    session.commit()
else:
    print "Skipping admin user create"


# categories insertion
print "Inserting parent categories"

# 0
parent = Categories(id=0, name="Parent Category", hasChildren=True)
session.add(parent)

# 1
sports = Categories(name="Sports and Outdoors", hasChildren=True, parent=0)
session.add(sports)

# 2
hgt = Categories(name="Home, Garden and Tools", hasChildren=True, parent=0)
session.add(hgt)

# 3
ec = Categories(name="Electronics and Computers", hasChildren=True, parent=0)
session.add(ec)
session.commit()

# inserting sub categories

print "Inserting sub-categories"
# 4
soccer = Categories(name="Soccer", hasChildren=False, parent=1)
session.add(soccer)
# 5
basketball = Categories(name="Basketball", hasChildren=False, parent=1)
session.add(basketball)
# 6
baseball = Categories(name="Baseball", hasChildren=False, parent=1)
session.add(baseball)
# 7
snowboarding = Categories(name="Snowboarding", hasChildren=False, parent=1)
session.add(snowboarding)
# 8
skating = Categories(name="Skating", hasChildren=False, parent=1)
session.add(skating)

# 9
knd = Categories(name="Kitchen and Dining", hasChildren=False, parent=2)
session.add(knd)
# 10
Appliances = Categories(name="Appliances", hasChildren=False, parent=2)
session.add(Appliances)

# 11
ha = Categories(name="Home Automation", hasChildren=False, parent=2)
session.add(ha)

# 12
lpt = Categories(name="Laptops and Tablets", hasChildren=False, parent=3)
session.add(lpt)

# 13
tv = Categories(name="TV and Video", hasChildren=False, parent=3)
session.add(tv)

# 14
vgame = Categories(name="Video Games", hasChildren=False, parent=3)
session.add(vgame)
# 15
headphones = Categories(name="Headphones", hasChildren=False, parent=3)
session.add(headphones)

session.commit()

# inserting test itemizes

hpItem = Items(name="Bose QuietComfort 15 Acoustic Noise Cancelling Headphones",
               description="These superbly-designed around-ear headphones feature exclusive Bose technologies. Not only do they fill your ears with dynamic, crystal-clear audio, they electronically sense the sounds around you and provide significant noise reduction across a wide range of frequencies. You'll enhance your listening experience with these comfortable and stylish QuietComfort headphones. When you fly, the engine roar fades even further away. When you listen to music at home or at work, fewer distractions get in the way. Less noise, along with acclaimed lifelike sound, a fit that stays comfortable for hours and the quality you expect from Bose. It all adds up to a better listening experience. They include two detachable cables, each with an integrated microphone and remote for convenient control of select iPod, iPhone and iPad models and Samsung Galaxy devices",
               pricerange="$230 - $299",
               pictureurl="http://scene7.samsclub.com/is/image/samsclub/0001781769174_A?wid=1500&hei=1500&fmt=jpg&qlt=80",
               category_id=15, user_id=1)
session.add(hpItem)


vgItem = Items(name="Tom Clancy's Rainbow Six Siege - Xbox One",
               description="The Rules of Siege: Five versus Five. Infiltrate versus Fortify. Team-based strategy meets intense, tactical combat.World's Elite Counter-Terrorist Operators: Choose your Operator. Wield their power. Unique abilities allow you to Attack or Defend your way.Singleplayer, Multiplayer, or Co-op: Terrorist Hunt is back! Stop the White Masks terrorist threat alone or with friends.Upgrade to Gold Edition: Includes game and Season Pass, which gives all fans and newcomers an extended Rainbow Six Siege experience.",
               pricerange="$59 - $60",
               pictureurl="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTDDGkfuw79IL2uHVqZ1cUi04gWkOVrYCCk9i7FNP_ePXb-p2bdqg",
               category_id=14, user_id=1)
session.add(vgItem)


tvItem = Items(name="TCL 48FS3700 48-Inch 1080p Roku Smart LED TV (2015 Model)",
               description="Refresh Rate: 60Hz (Native), 120Hz Clear Motion Index (Effective)Backlight: LED (Full Array)Smart Functionality: Yes - Roku TV Streaming Platform",
               pricerange="$379 - $400",
               pictureurl="http://ecx.images-amazon.com/images/I/81GxQG2cNwL._SX466_.jpg",
               category_id=13, user_id=1)
session.add(tvItem)


lptItem = Items(name="ASUS Chromebook 13-Inch HD with Gigabit WiFi, 16GB Storage and 4GB RAM (Black)",
                description="10 Hours Incredible Battery Life. Gigabit Dual-Band 802.11AC ultra-fast Wi-Fi.Can open/edit MS Office files using free embedded QuickOffice editor or Google Docs, and can download Microsoft Office Online (an online version of Microsoft Office) for free. Cannot install standard MS Office software.",
                pricerange="$189 - $200",
                pictureurl="http://ecx.images-amazon.com/images/I/81CwszuAf2L._SX522_.jpg",
                category_id=12, user_id=1)
session.add(lptItem)


haItem = Items(name="GE Link, Wireless A19 Smart Connected LED Light Bulb, Soft White (2700K), 60-Watt Equivalent, 1-Pack",
               description="Compatible with Wink App and Amazon Echo (requires Wink HUB) Provides 800 lumens of light output Estimated yearly energy costs $1.45 based on 3 hours per day $0.11 per kWh 1 bulb per package with 2700K light appearance",
               pricerange="$14 - $49",
               pictureurl="http://g-ecx.images-amazon.com/images/G/01/aplusautomation/vendorimages/c0709e5a-0bd6-4b32-8580-609964b3397a._CB319628893__SR300,300_.jpg",
               category_id=11, user_id=1)
session.add(haItem)


appItem = Items(name="Cuisinart DLC-2009CHBM Prep 9 9-Cup Food Processor, Brushed Stainless",
                description="Brushed Stainless Steel housing for enhanced durability. Lexan work bowl virtually shatterproof, dishwasher-safe. Speed automatically adjusts to ensure proper dough consistency; does not include DVD and the blade. Includes spatula, recipe/instruction book, and dishwasher-safe parts",
                pricerange="$119 - $149",
                pictureurl="http://images.prod.meredith.com/product/3b1223791316e1b9aa96341b6e9b8f0b/7a1c7008467be8b8a011fcff24fdf8e0b54132937d5dd1f21efa0811e8b4c932/l/cuisinart-dlc-2009chbm-prep-9-9-cup-food-processor-brushed-stainless",
                category_id=10, user_id=1)
session.add(appItem)

kndItem = Items(name="Victorinox Swiss Army 8-Inch Fibrox Straight Edge Chef's Knife",
                description="8-inch multipurpose chef's knife designed for chopping, mincing, slicing, and dicing. High-carbon stainless steel blade provides maximum sharpness and edge retention. Blade is conical ground lengthwise and crosswise for minimal resistance while cutting, laser tested to ensure optimum cutting power.Swiss item #5.2063.20 printed on the Blade.",
                pricerange="$32 - $53",
                pictureurl="http://ecx.images-amazon.com/images/I/41gmrqbmyYL._SY300_.jpg",
                category_id=9, user_id=1)
session.add(kndItem)


skatingItem = Items(name="AandR Sports Deluxe Skate Bag",
                    description="Two Large Compartments for Ice Skates or Roller Blades. Additional Compartment to Store Accessories. Adjustable Shoulder Strap. From AandR Sports, the leading brand in sports accessories for over 20 years",
                    pricerange="$26 - $28",
                    pictureurl="http://ecx.images-amazon.com/images/I/71Eb90TnV2L._SL1000_.jpg",
                    category_id=8, user_id=1)
session.add(skatingItem)


snowboardingItem = Items(name="Lucky Bums Plastic Snowboard",
                         description="Beginner snowboard is great choice to introduce kids to snowboarding in backyard or on nearby sledding hill. Smooth bottom board with traditional snowboard cut. Rugged design includes pre-mounted adjustable bindings that accommodate snow boots; durable latch system ensures secure fit. Recommended for riders age nine and up; since it does not include metal edges, snowboard not recommended for ski resort use. Limited lifetime manufacturer's warranty against defects in materials and workmanship",
                         pricerange="$44 - $164",
                         pictureurl="http://wildchildsports.com/wp-content/uploads/2014/10/lucky-bums-snowboard.jpg",
                         category_id=7, user_id=1)
session.add(snowboardingItem)


baseballItem = Items(name="Rawlings Baseball Official League 9 In. Solid Cork and Rubber Center 5 Oz",
                     description="Official size 9. *Weight 5 oz. *Synthetic cover.*Solid cork & rubber center.*Major league seam",
                     pricerange="$6 - $7",
                     pictureurl="http://ecx.images-amazon.com/images/I/51VGMBD3NYL._SY355_.jpg",
                     category_id=6, user_id=1)
session.add(baseballItem)


basketballItem = Items(name="Spalding NBA Street Basketball",
                       description="Ultra-durable, performance rubber cover. Designed to withstand the rough-and-tumble street game. Wide channel design for excellent grip. Features the NBA logo",
                       pricerange="$11 - $115",
                       pictureurl="http://ecx.images-amazon.com/images/I/61VHXIXK6JL._SX300_.jpg",
                       category_id=5, user_id=1)
session.add(basketballItem)

scocerItem = Items(name="adidas Performance Conext15 Glider Soccer Ball",
                   description="High quality with exceptional durability. Butyl bladder for best air and shape retention. Machine-stitched construction with nylon wound carcass. TPU construction for soft touch and high durability. 100% Butylene injection molded",
                   pricerange="$10 - $50",
                   pictureurl="http://ecx.images-amazon.com/images/I/51VrfN5VwrL._SY355_.jpg",
                   category_id=4, user_id=1)
session.add(scocerItem)

session.commit();
