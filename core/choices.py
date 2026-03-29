from django.db import models

# ================================
# ALL CONVERTED TO TextChoices
# ================================

class StaffRoleChoice(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    MANAGER = 'Manager', 'Manager'
    EMPLOYEE = 'Employee', 'Employee'
    VENDOR = 'Vendor', 'Vendor'
    CUSTOMER = 'Customer', 'Customer'
    MEMBER = 'Member', 'Member'
    RIDER = 'Rider', 'Rider'
    TRADER = 'Trader', 'Trader'

class GenderChoice(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'

class CountryChoice(models.TextChoices):
    # Unique ISO Key = 'Unique ISO Key', 'Display Label'
    AF = 'AF', 'Afghanistan (+93)'
    AL = 'AL', 'Albania (+355)'
    DZ = 'DZ', 'Algeria (+213)'
    AR = 'AR', 'Argentina (+54)'
    AU = 'AU', 'Australia (+61)'
    AT = 'AT', 'Austria (+43)'
    BD = 'BD', 'Bangladesh (+880)'
    BE = 'BE', 'Belgium (+32)'
    BR = 'BR', 'Brazil (+55)'
    CA = 'CA', 'Canada (+1)'
    CN = 'CN', 'China (+86)'
    CO = 'CO', 'Colombia (+57)'
    DK = 'DK', 'Denmark (+45)'
    EG = 'EG', 'Egypt (+20)'
    FI = 'FI', 'Finland (+358)'
    FR = 'FR', 'France (+33)'
    DE = 'DE', 'Germany (+49)'
    GH = 'GH', 'Ghana (+233)'
    GR = 'GR', 'Greece (+30)'
    IN = 'IN', 'India (+91)'
    ID = 'ID', 'Indonesia (+62)'
    IE = 'IE', 'Ireland (+353)'
    IT = 'IT', 'Italy (+39)'
    JP = 'JP', 'Japan (+81)'
    KE = 'KE', 'Kenya (+254)'
    MY = 'MY', 'Malaysia (+60)'
    MX = 'MX', 'Mexico (+52)'
    NL = 'NL', 'Netherlands (+31)'
    NG = 'NG', 'Nigeria (+234)'
    NO = 'NO', 'Norway (+47)'
    PK = 'PK', 'Pakistan (+92)'
    PH = 'PH', 'Philippines (+63)'
    PL = 'PL', 'Poland (+48)'
    PT = 'PT', 'Portugal (+351)'
    RU = 'RU', 'Russia (+7)'
    SA = 'SA', 'Saudi Arabia (+966)'
    SG = 'SG', 'Singapore (+65)'
    ZA = 'ZA', 'South Africa (+27)'
    KR = 'KR', 'South Korea (+82)'
    ES = 'ES', 'Spain (+34)'
    LK = 'LK', 'Sri Lanka (+94)'
    SE = 'SE', 'Sweden (+46)'
    CH = 'CH', 'Switzerland (+41)'
    TH = 'TH', 'Thailand (+66)'
    TR = 'TR', 'Turkey (+90)'
    UA = 'UA', 'Ukraine (+380)'
    AE = 'AE', 'United Arab Emirates (+971)'
    GB = 'GB', 'United Kingdom (+44)'
    US = 'US', 'United States (+1)'
    VN = 'VN', 'Vietnam (+84)'

    @classmethod
    def get_dial_code(cls, iso_code):
        """Returns the dial code for a given ISO key"""
        codes = {
            'AF': '+93', 'AL': '+355', 'DZ': '+213', 'AR': '+54', 'AU': '+61', 
            'AT': '+43', 'BD': '+880', 'BE': '+32', 'BR': '+55', 'CA': '+1', 
            'CN': '+86', 'CO': '+57', 'DK': '+45', 'EG': '+20', 'FI': '+358', 
            'FR': '+33', 'DE': '+49', 'GH': '+233', 'GR': '+30', 'IN': '+91', 
            'ID': '+62', 'IE': '+353', 'IT': '+39', 'JP': '+81', 'KE': '+254', 
            'MY': '+60', 'MX': '+52', 'NL': '+31', 'NG': '+234', 'NO': '+47', 
            'PK': '+92', 'PH': '+63', 'PL': '+48', 'PT': '+351', 'RU': '+7', 
            'SA': '+966', 'SG': '+65', 'ZA': '+27', 'KR': '+82', 'ES': '+34', 
            'LK': '+94', 'SE': '+46', 'CH': '+41', 'TH': '+66', 'TR': '+90', 
            'UA': '+380', 'AE': '+971', 'GB': '+44', 'US': '+1', 'VN': '+84',
        }
        return codes.get(iso_code, "")

        
class SocialMediaChoice(models.TextChoices):
    GMAIL = 'GMAIL', 'Gmail'
    FACEBOOK = 'FACEBOOK', 'Facebook'
    INSTAGRAM = 'INSTAGRAM', 'Instagram'
    LINKEDIN = 'LINKEDIN', 'LinkedIn'
    PHONE = 'PHONE', 'Phone'
    TWITTER = 'TWITTER', 'Twitter'
    YOUTUBE = 'YOUTUBE', 'YouTube'
    WHATSAPP = 'WHATSAPP', 'WhatsApp'
    HOME_PAGE_WHATSAPP = 'HOME_PAGE_WHATSAPP', 'Home Page WhatsApp'
    HOME_PAGE_PHONE = 'HOME_PAGE_PHONE', 'Home Page Phone'
    HOME_PAGE_INSTAGRAM = 'HOME_PAGE_INSTAGRAM', 'Home Page Instagram'
    HOME_PAGE_GMAIL = 'HOME_PAGE_GMAIL', 'Home Page Gmail'

class AlertTypeChoice(models.TextChoices):
    SUBSCRIPTION_EXPIRED = 'subscription_expired', 'Subscription Expired'
    SUBSCRIPTION_REMINDER = 'subscription_reminder', 'Subscription Reminder'
    GENERAL = 'general', 'General Alert'

class SessionStatusChoice(models.TextChoices):
    UPCOMING = 'upcoming', 'Upcoming'
    LIVE = 'live', 'Live'
    ENDED = 'ended', 'Ended'

class AttendanceStatusChoice(models.TextChoices):
    CHECKED_IN = 'checked_in', 'Checked In'
    CHECKED_OUT = 'checked_out', 'Checked Out'
    AUTO_CHECKED_OUT = 'auto_checked_out', 'Auto Checked Out'

class GoalChoice(models.TextChoices):
    WEIGHT_LOSS = 'weight_loss', 'Weight Loss'
    WEIGHT_GAIN = 'weight_gain', 'Weight Gain'
    COMPETITION = 'competition', 'Competition'
    BASIC_MAINTENANCE = 'basic_maintenance', 'Basic Maintenance'

class LevelChoice(models.TextChoices):
    BEGINNER = 'beginner', 'Beginner'
    MEDIUM = 'medium', 'Medium'
    ADVANCED = 'advanced', 'Advanced'
    MASTER = 'master', 'Master'

class WeekdayChoice(models.TextChoices):
    MONDAY = 'monday', 'Monday'
    TUESDAY = 'tuesday', 'Tuesday'
    WEDNESDAY = 'wednesday', 'Wednesday'
    THURSDAY = 'thursday', 'Thursday'
    FRIDAY = 'friday', 'Friday'
    SATURDAY = 'saturday', 'Saturday'
    SUNDAY = 'sunday', 'Sunday'

class ActivityTypeChoice(models.TextChoices):
    EXERCISE = 'exercise', 'Exercise'
    CARDIO = 'cardio', 'Cardio'
    CIRCUIT = 'circuit', 'Circuit'
    REST = 'rest', 'Rest'

class WorkoutStatusChoice(models.TextChoices):
    ASSIGNED = 'assigned', 'Assigned'
    ACTIVE = 'active', 'Active'
    COMPLETED = 'completed', 'Completed'
    PAUSED = 'paused', 'Paused'

class PackageTypeChoice(models.TextChoices):
    MONTHLY = 'monthly', 'Monthly'
    QUARTERLY = 'quarterly', 'Quarterly'
    YEARLY = 'yearly', 'Yearly'
    CUSTOM = 'custom', 'Custom'

class DiscountTypeChoice(models.TextChoices):
    NONE = 'none', 'None'
    FLAT = 'flat', 'Flat Amount'
    PERCENT = 'percent', 'Percentage'

class PaymentActionChoice(models.TextChoices):
    INITIATE = 'INITIATE', 'Initiate Payment'
    FETCH_SESSION = 'FETCH_SESSION', 'Fetch Session'
    GET_ORDER = 'GET_ORDER', 'Get Existing Order'
    CREATE_LINK = 'CREATE_LINK', 'Create Payment Link'
    WEBHOOK = 'WEBHOOK', 'Webhook'
    ERROR = 'ERROR', 'Error'  # ✅ FIXED SYNTAX

class TransactionTypeChoice(models.TextChoices):
    INCOME = 'income', 'Income'
    EXPENSE = 'expense', 'Expense'

class TransactionCategoryChoice(models.TextChoices):
    SALES = 'sales', 'Sales'
    REFUND = 'refund', 'Refund'
    SALARY = 'salary', 'Salary'
    RENT = 'rent', 'Rent'
    UTILITIES = 'utilities', 'Utilities'
    MARKETING = 'marketing', 'Marketing'
    INVENTORY = 'inventory', 'Inventory'
    OTHER = 'other', 'Other'

class TransactionStatusChoice(models.TextChoices):
    INITIATED = 'initiated', 'Initiated'
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    REFUNDED = 'refunded', 'Refunded'

class PaymentStatusChoice(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'


class TicketStatusChoice(models.TextChoices):
    OPEN = 'open', 'Open'
    IN_PROGRESS = 'in_progress', 'In Progress'
    RESOLVED = 'resolved', 'Resolved'
    CLOSED = 'closed', 'Closed'

class EnquiryStatusChoice(models.TextChoices):
    NEW = 'new', 'New'
    CONTACTED = 'contacted', 'Contacted'
    IN_PROGRESS = 'in_progress', 'In Progress'
    RESOLVED = 'resolved', 'Resolved'
    CLOSED = 'closed', 'Closed'


class SubscriptionStatusChoice(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACTIVE = 'active', 'Active'
    EXPIRED = 'expired', 'Expired'
    CANCELLED = 'cancelled', 'Cancelled'

class DriverStatusChoice(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    BUSY = 'busy', 'Busy'
    OFFLINE = 'offline', 'Offline'  

class RideStatusChoice(models.TextChoices):
    REQUESTED = 'requested', 'Requested'
    ACCEPTED = 'accepted', 'Accepted'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'

class VehicleTypeChoice(models.TextChoices):
    BIKE = 'bike', 'Bike'
    SCOOTER = 'scooter', 'Scooter'
    BICYCLE = 'bicycle', 'Bicycle'
    CAR = 'car', 'Car'



class CustomerAddressTypeChoice(models.TextChoices):
    HOME = 'home', 'Home'
    WORK = 'work', 'Work'
    OTHER = 'other', 'Other'


class OrderStatusChoice(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    PREPARING = 'preparing', 'Preparing'
    READY_FOR_PICKUP = 'ready_for_pickup', 'Ready for Pickup'
    ASSIGNED_RIDER = 'assigned_rider', 'Assigned to Rider'
    PICKED_UP = 'picked_up', 'Picked Up'
    OUT_FOR_DELIVERY = 'out_for_delivery', 'Out for Delivery'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'
    REFUNDED = 'refunded', 'Refunded'


class PaymentMethodChoice(models.TextChoices):
    COD = 'cod', 'Cash on Delivery'
    ONLINE = 'online', 'Online Payment'
    WALLET = 'wallet', 'Wallet'



class ReviewTypeChoice(models.TextChoices):
    PRODUCT = 'product', 'Product Review'
    VENDOR = 'vendor', 'Vendor Review'
    RIDER = 'rider', 'Rider Review'