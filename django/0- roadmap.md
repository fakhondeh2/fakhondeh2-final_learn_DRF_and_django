### Django Fundamentals

**Django Project Setup**
- Install Django
- Create a Project
- Create an Application
- Configure Settings
- Database Setup
- Run Migrations
- Understand MVT
- URL Routing

**Django Models**
- Define Modelsd
- Model Fields
- Relationships
- Custom Managers
- Model Inheritance
- QuerySets
- Database Migrations
- Admin Interface

**Django Views and URLs**
- Function-Based Views
- Class-Based Views
- URL Dispatcher
- URL Patterns
- Path Converters
- Reverse URL Lookup
- Request-Response Cycle
- HTTP Methods

---

### REST API Core Concepts

**REST Principles**
- Client-Server Architecture
- Statelessness
- Cacheability
- Layered System
- Uniform Interface
- Resource Identification
- Resource Manipulation
- Hypermedia as Engine

**HTTP Methods**
- GET for Retrieval
- POST for Creation
- PUT for Full Update
- PATCH for Partial Update
- DELETE for Deletion
- Idempotency
- Safe Methods
- Request and Response

**JSON Data Format**
- JSON Syntax
- Objects and Arrays
- Data Types
- Serialization
- Deserialization
- Nesting JSON
- JSON Schema
- JSON Validation

---

### DRF Basics

**DRF Installation Setup**
- Install Django REST Framework
- Add to Installed Apps
- Basic Settings
- Project Configuration
- View DRF Admin
- Initializing Routers
- First API View
- Testing Setup

**Serializers**
- Model Serializers
- Field Types
- Custom Fields
- Validation
- Data Representation
- Nested Serializers
- List Serializers
- Writeable Nested Serializers

---

### DRF Views and ViewSets

**Class-Based Views**
- APIView
- Generic API Views
- ListAPIView
- CreateAPIView
- RetrieveAPIView
- UpdateAPIView
- DestroyAPIView
- ListCreateAPIView

**ViewSets and Routers**
- ModelViewSet
- ReadOnlyModelViewSet
- Custom ViewSets
- Default Router
- Simple Router
- Registering ViewSets
- URL Generation
- Action Decorators

**Mixins**
- ListModelMixin
- CreateModelMixin
- RetrieveModelMixin
- UpdateModelMixin
- DestroyModelMixin
- Combined Mixins
- Custom Mixins
- Mixin Order

**Generic View Customization**
- Queryset Override
- Serializer Class Override
- Permission Classes
- Authentication Classes
- Pagination Classes
- Filter Backend Classes
- Lookup Field
- perform_create Method

---

### DRF Filtering and Pagination

**Filtering Data**
- DjangoFilterBackend
- FilterSet Definition
- Field Lookups
- Range Filters
- OrderingFilter
- SearchFilter
- Custom Filters
- Multiple Filters

**Pagination**
- PageNumberPagination
- LimitOffsetPagination
- CursorPagination
- Custom Pagination
- Page Size Control
- Pagination Links
- Global Pagination Settings
- Per-View Pagination

---

### DRF Authentication and Permissions

**Session Authentication**
- Django Sessions
- Login and Logout
- CsrfViewMiddleware
- SessionBackend
- Session Login View
- Cookie-Based Auth
- Advantages and Disadvantages
- Integration with DRF

**JWT Authentication**
- Install djangorestframework-simplejwt
- Configure Settings
- Obtain Token View
- Refresh Token View
- Verify Token View
- Blacklisting Tokens
- Customizing JWT Payload
- Token Lifespan

**Permissions**
- IsAuthenticated
- AllowAny
- IsAdminUser
- IsAuthenticatedOrReadOnly
- Custom Permissions
- Object-Level Permissions
- HasObjectPermission
- Permission Ordering

---

### Advanced Serializers

**Custom Serializer Fields**
- SerializerMethodField
- CharField Customization
- FileField Usage
- ImageField Usage
- Read-Only Fields
- Write-Only Fields
- HiddenField
- Custom Validators

**Nested Serializers**
- Read-Only Nested
- Writeable Nested
- many=True Nested
- Source Attribute
- create Method Override
- update Method Override
- Nested Validation
- Depth Option

**File Uploads**
- FileUploadParser
- MultiPartParser
- File Storage Backend
- FileField in Serializer
- Handling Uploaded Files
- Request.FILES Access
- File Size Validation
- Image Processing Libraries

---

### DRF Testing

**Unit Testing Basics**
- TestCase Class
- APITestCase Class
- Test Client
- Request Factory
- Assertions
- Setup and Teardown
- Test Naming
- Running Tests

**Serializer Testing**
- Test Valid Data
- Test Invalid Data
- Test Serialization
- Test Deserialization
- Test create Method
- Test update Method
- Edge Cases
- Fixtures

**View and ViewSet Testing**
- Test GET Requests
- Test POST Requests
- Test PUT Requests
- Test DELETE Requests
- Test Authentication
- Test Permissions
- Test Filtering
- Test Pagination

---

### DRF Advanced Features

**Routers Customization**
- Custom Router Class
- Custom Base Name
- Router Registration
- Router Methods
- Dynamic URL Routes
- Nested Routers
- Extra Routes
- Custom Actions

**Signals**
- pre_save Signal
- post_save Signal
- pre_delete Signal
- post_delete Signal
- Custom Signals
- Connecting Receivers
- Dispatching Signals
- Signal Arguments

---

### Database Management

**PostgreSQL Integration**
- Install psycopg2
- Database Settings
- Connection Pooling
- User and Permissions
- Schema Management
- Indexing
- Stored Procedures
- Performance Tuning Basics

**Redis Caching**
- Install django-redis
- Cache Backend Setup
- Cache Decorators
- cache.set
- cache.get
- cache.delete
- Cache Invalidation
- Low-Level Cache API

---

### Error Handling

**Exception Handling**
- APIException
- Custom Exception Classes
- exception_handler
- set_rollback
- Debug Mode Behavior
- HTTP Status Codes
- Error Responses
- Logging Exceptions

**Validation Errors**
- Serializer is_valid
- ValidationError
- Field-Level Errors
- Non-Field Errors
- Custom Validators
- Error Message Customization
- Global Validation Handling
- Error Response Format

---

### API Versioning

**URL Versioning**
- URL Patterns
- URLPathVersioning
- Versioning Regular Expressions
- Pros and Cons
- Example Implementations
- Deprecating Versions
- API Gateway Considerations
- Client Compatibility

**Namespace Versioning**
- Django URL Namespaces
- NamespaceVersioning
- URL Prefixing
- Versioning with Routers
- Managing Multiple Versions
- Migration Strategies
- Documentation for Versions
- Client-Side Versioning