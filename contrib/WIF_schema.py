import sgqlc.types
import sgqlc.types.datetime
import sgqlc.types.relay


WIF_schema = sgqlc.types.Schema()


# Unexport Node/PageInfo, let schema re-declare them
WIF_schema -= sgqlc.types.relay.Node
WIF_schema -= sgqlc.types.relay.PageInfo



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

class Certification(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('IATF_16949', 'ISO_14001', 'ISO_9001')


DateTime = sgqlc.types.datetime.DateTime

class ErrorCodes(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('AUTHENTICATION', 'AUTHORISATION', 'BAD_REQUEST', 'BILLING_CARD_DECLINED', 'BILLING_ERROR', 'INVITE_ERROR', 'NOTFOUND', 'NO_BOT', 'PROJECT_PAYMENT_OVERDUE', 'REDIRECT', 'UNHANDLED_ERROR', 'USER_MISMATCH', 'USER_NOT_CONFIRMED', 'VALIDATION')


Float = sgqlc.types.Float

ID = sgqlc.types.ID

class ImportUrlString(sgqlc.types.Scalar):
    __schema__ = WIF_schema


Int = sgqlc.types.Int

class JSONString(sgqlc.types.Scalar):
    __schema__ = WIF_schema


class MinMaxType(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('MAX', 'MIN')


class NotificationType(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('COMMENTED', 'CREATED', 'FOLLOWED', 'HTML', 'INVITED', 'INVITE_ACTIONED', 'LIKED', 'MENTIONED')


class Operator(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('CONTAINS', 'EQ', 'GTE', 'LTE')


class OptionValueType(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('BOOL', 'FLOAT', 'INT', 'STRING')


class OrderStatus(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('CANCELLED', 'CONFIRMED', 'CREATED', 'PRODUCED', 'SHIPPED', 'STARTED')


class PaymentStatus(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('INITIALIZED', 'PAIDFULL', 'PAIDPARTIAL', 'REFUNDED')


class Permission(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('ADD_ANNOTATION', 'ADD_MESSAGE', 'DELETE_ANNOTATION', 'DELETE_MESSAGE', 'GET_ANNOTATION', 'GET_MESSAGE', 'UPDATE_ANNOTATION', 'UPDATE_MESSAGE')


class QuotingPriority(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('CUSTOM', 'PRICE', 'PROXIMITY', 'QUALITY', 'SPEED')


class RequestForQuoteState(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('ASSIGNED', 'AWARDED', 'CANCELLED', 'COMPLETED', 'INCOMPLETE', 'INITIATED', 'QUOTED')


class RequestForQuoteType(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('DIRECT', 'INTERMEDIATED')


class SessionState(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('APPROVED', 'CLOSED', 'OPEN')


class SortOrder(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('ASC', 'DESC')


class Status(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('ADDED', 'MODIFIED', 'REMOVED')


String = sgqlc.types.String

Time = sgqlc.types.datetime.Time

class ValueInputType(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('BOOL', 'DATETIME', 'FLOAT', 'INT', 'STRING')


class plantype(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('BY_SEATS', 'FLAT')


class project_type(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('PROJECT', 'RFQ', 'SHARED_FILE')


class subscriptionstatus(sgqlc.types.Enum):
    __schema__ = WIF_schema
    __choices__ = ('ACTIVE', 'CANCELED', 'INCOMPLETE')



########################################################################
# Input Objects
########################################################################
class AcceptInviteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('invite_id', 'referrer_user_id', 'token')
    invite_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='inviteId')
    referrer_user_id = sgqlc.types.Field(ID, graphql_name='referrerUserId')
    token = sgqlc.types.Field(String, graphql_name='token')


class AddPaymentMethodInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space_slug', 'stripe_token')
    space_slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='spaceSlug')
    stripe_token = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='stripeToken')


class ApproveSessionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('session_id',)
    session_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='sessionId')


class AssignRequestForQuoteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('request_for_quote_id', 'manufacturer_id')
    request_for_quote_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='requestForQuoteId')
    manufacturer_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='manufacturerId')


class BanProfileInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('username', 'banned')
    username = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='username')
    banned = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='banned')


class BillingAddSeatsInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('subscription_id', 'add_nseats')
    subscription_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='subscriptionId')
    add_nseats = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='addNSeats')


class BillingCancelSubscriptionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('subscription_id',)
    subscription_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='subscriptionId')


class BillingRemoveSeatsInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('subscription_id', 'remove_nseats')
    subscription_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='subscriptionId')
    remove_nseats = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='removeNSeats')


class BillingSubscribeInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space_slug', 'card_id', 'country_code', 'coupon', 'tax_id', 'extra_seats', 'start_free_trial')
    space_slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='spaceSlug')
    card_id = sgqlc.types.Field(ID, graphql_name='cardId')
    country_code = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='countryCode')
    coupon = sgqlc.types.Field(String, graphql_name='coupon')
    tax_id = sgqlc.types.Field(ID, graphql_name='taxId')
    extra_seats = sgqlc.types.Field(Int, graphql_name='extraSeats')
    start_free_trial = sgqlc.types.Field(Boolean, graphql_name='startFreeTrial')


class CameraInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('up', 'right', 'position', 'lookat')
    up = sgqlc.types.Field(sgqlc.types.non_null('VectorInput'), graphql_name='up')
    right = sgqlc.types.Field(sgqlc.types.non_null('VectorInput'), graphql_name='right')
    position = sgqlc.types.Field(sgqlc.types.non_null('VectorInput'), graphql_name='position')
    lookat = sgqlc.types.Field(sgqlc.types.non_null('VectorInput'), graphql_name='lookat')


class CancelImportProjectInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('project_id',)
    project_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='projectId')


class CancelOrderInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('order_id',)
    order_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='orderId')


class CategoryInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('forum_id', 'title', 'description', 'color')
    forum_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='forumId')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    color = sgqlc.types.Field(String, graphql_name='color')


class CertificateInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'file_id')
    name = sgqlc.types.Field(sgqlc.types.non_null(Certification), graphql_name='name')
    file_id = sgqlc.types.Field(String, graphql_name='fileId')


class ChangeEmailPreferencesInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'enabled')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')


class ChangeLanguagePreferencesInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('locale',)
    locale = sgqlc.types.Field(String, graphql_name='locale')


class ChangePasswordInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('current_password', 'new_password')
    current_password = sgqlc.types.Field(String, graphql_name='currentPassword')
    new_password = sgqlc.types.Field(String, graphql_name='newPassword')


class CloseRequestForQuoteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('request_for_quote_id', 'keep_session_ids')
    request_for_quote_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='requestForQuoteId')
    keep_session_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='keepSessionIds')


class CloseSessionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('session_id',)
    session_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='sessionId')


class CollectionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'name', 'description', 'tags', 'projects')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    tags = sgqlc.types.Field(sgqlc.types.list_of('TagInput'), graphql_name='tags')
    projects = sgqlc.types.Field(sgqlc.types.list_of('CollectionProjectInput'), graphql_name='projects')


class CollectionProjectInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'project_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='projectId')


class CommentInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'body', 'origin', 'replyto')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    body = sgqlc.types.Field(String, graphql_name='body')
    origin = sgqlc.types.Field(ID, graphql_name='origin')
    replyto = sgqlc.types.Field(ID, graphql_name='replyto')


class CommitInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('project_id', 'title', 'description', 'conflicts_resolution', 'conflicts_parent')
    project_id = sgqlc.types.Field(ID, graphql_name='projectId')
    title = sgqlc.types.Field(String, graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    conflicts_resolution = sgqlc.types.Field(sgqlc.types.list_of('ConflictResolutionInput'), graphql_name='conflictsResolution')
    conflicts_parent = sgqlc.types.Field(String, graphql_name='conflictsParent')


class ConfirmOrderInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('order_id',)
    order_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='orderId')


class ConfirmProfileInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('username', 'full_name', 'bio', 'avatar', 'intent_id', 'user_type_id', 'email')
    username = sgqlc.types.Field(String, graphql_name='username')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    avatar = sgqlc.types.Field(ID, graphql_name='avatar')
    intent_id = sgqlc.types.Field(ID, graphql_name='intentId')
    user_type_id = sgqlc.types.Field(ID, graphql_name='userTypeId')
    email = sgqlc.types.Field(String, graphql_name='email')


class ConflictResolutionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('path', 'picked_file_id')
    path = sgqlc.types.Field(String, graphql_name='path')
    picked_file_id = sgqlc.types.Field(ID, graphql_name='pickedFileId')


class ConversionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('original_file_id', 'conversion_type', 'json_info', 'converted_file_id', 'viewer_semver')
    original_file_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='originalFileId')
    conversion_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='conversionType')
    json_info = sgqlc.types.Field(String, graphql_name='jsonInfo')
    converted_file_id = sgqlc.types.Field(ID, graphql_name='convertedFileId')
    viewer_semver = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='viewerSemver')


class ConvertAssemblyInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('file_id', 'format')
    file_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='fileId')
    format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='format')


class CreateAddressInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'address1', 'address2', 'city', 'province', 'country', 'zip', 'company', 'phone', 'space_id', 'default')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    address1 = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='address1')
    address2 = sgqlc.types.Field(String, graphql_name='address2')
    city = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='city')
    province = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='province')
    country = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='country')
    zip = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='zip')
    company = sgqlc.types.Field(String, graphql_name='company')
    phone = sgqlc.types.Field(String, graphql_name='phone')
    space_id = sgqlc.types.Field(String, graphql_name='spaceId')
    default = sgqlc.types.Field(Boolean, graphql_name='default')


class CreateAnnotationInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('context_id', 'resource_id', 'body', 'target', 'camera', 'hoops_version', 'import_config', 'temp_key')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextId')
    resource_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='resourceId')
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='body')
    target = sgqlc.types.Field(sgqlc.types.non_null('TargetInput'), graphql_name='target')
    camera = sgqlc.types.Field(sgqlc.types.non_null(CameraInput), graphql_name='camera')
    hoops_version = sgqlc.types.Field(String, graphql_name='hoopsVersion')
    import_config = sgqlc.types.Field(String, graphql_name='importConfig')
    temp_key = sgqlc.types.Field(String, graphql_name='tempKey')


class CreateAssemblyInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('file_id', 'hashes')
    file_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='fileId')
    hashes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='hashes')


class CreateBuildInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('file_id', 'material_id', 'process_id', 'build_value_inputs')
    file_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='fileId')
    material_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='materialId')
    process_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='processId')
    build_value_inputs = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('CreateBuildValueInput')), graphql_name='buildValueInputs')


class CreateBuildValueInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('option_id', 'value_float', 'value_int', 'value_string', 'value_bool')
    option_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='optionId')
    value_float = sgqlc.types.Field(Float, graphql_name='valueFloat')
    value_int = sgqlc.types.Field(Int, graphql_name='valueInt')
    value_string = sgqlc.types.Field(String, graphql_name='valueString')
    value_bool = sgqlc.types.Field(Boolean, graphql_name='valueBool')


class CreateIntermediatorInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('enquiry_email', 'initiative_id', 'space_id', 'address')
    enquiry_email = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='enquiryEmail')
    initiative_id = sgqlc.types.Field(ID, graphql_name='initiativeId')
    space_id = sgqlc.types.Field(ID, graphql_name='spaceId')
    address = sgqlc.types.Field(sgqlc.types.non_null(CreateAddressInput), graphql_name='address')


class CreateInviteLinkInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space_slug', 'slug', 'expires_in_days')
    space_slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='spaceSlug')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    expires_in_days = sgqlc.types.Field(Int, graphql_name='expiresInDays')


class CreateJobSpecInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('build', 'quantity', 'shipping_address')
    build = sgqlc.types.Field(sgqlc.types.non_null(CreateBuildInput), graphql_name='build')
    quantity = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='quantity')
    shipping_address = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='shippingAddress')


class CreateManufacturerInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('enquiry_email', 'initiative_id', 'space_id', 'address', 'ships_to', 'telephone', 'founding_year', 'industries', 'num_employees', 'num_machines', 'lead_time', 'file_formats', 'case_studies', 'company_type')
    enquiry_email = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='enquiryEmail')
    initiative_id = sgqlc.types.Field(ID, graphql_name='initiativeId')
    space_id = sgqlc.types.Field(ID, graphql_name='spaceId')
    address = sgqlc.types.Field(sgqlc.types.non_null(CreateAddressInput), graphql_name='address')
    ships_to = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='shipsTo')
    telephone = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='telephone')
    founding_year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='foundingYear')
    industries = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='industries')
    num_employees = sgqlc.types.Field(Int, graphql_name='numEmployees')
    num_machines = sgqlc.types.Field(Int, graphql_name='numMachines')
    lead_time = sgqlc.types.Field(String, graphql_name='leadTime')
    file_formats = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='fileFormats')
    case_studies = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='caseStudies')
    company_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='companyType')


class CreateMaterialsInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('material_inputs',)
    material_inputs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaterialInput'))), graphql_name='materialInputs')


class CreateMessageInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('body', 'context_id', 'reference_id', 'resource_id', 'temp_key')
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='body')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    reference_id = sgqlc.types.Field(String, graphql_name='referenceId')
    resource_id = sgqlc.types.Field(String, graphql_name='resourceId')
    temp_key = sgqlc.types.Field(String, graphql_name='tempKey')


class CreateMinMaxOptionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'type', 'for_id', 'value_type', 'step', 'required', 'unit', 'nil_label', 'prefix')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    type = sgqlc.types.Field(sgqlc.types.non_null(MinMaxType), graphql_name='type')
    for_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='forId')
    value_type = sgqlc.types.Field(sgqlc.types.non_null(OptionValueType), graphql_name='valueType')
    step = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='step')
    required = sgqlc.types.Field(Boolean, graphql_name='required')
    unit = sgqlc.types.Field(String, graphql_name='unit')
    nil_label = sgqlc.types.Field(String, graphql_name='nilLabel')
    prefix = sgqlc.types.Field(String, graphql_name='prefix')


class CreateOptionInstancesInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('manufacturer_id', 'option_id', 'process_id', 'material_ids', 'value_ints', 'value_floats', 'value_strings', 'value_bools')
    manufacturer_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='manufacturerId')
    option_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='optionId')
    process_id = sgqlc.types.Field(ID, graphql_name='processId')
    material_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='materialIds')
    value_ints = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name='valueInts')
    value_floats = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Float)), graphql_name='valueFloats')
    value_strings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='valueStrings')
    value_bools = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Boolean)), graphql_name='valueBools')


class CreateOrderInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('quote_id', 'shipping')
    quote_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='quoteId')
    shipping = sgqlc.types.Field(sgqlc.types.non_null('ShippingInput'), graphql_name='shipping')


class CreateProcessesInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('process_inputs',)
    process_inputs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ProcessInput'))), graphql_name='processInputs')


class CreateQuoteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('job_spec_id', 'cost', 'currency', 'material_id', 'process_id', 'manufacturer_id', 'valid_until', 'is_shipping_included', 'is_estimated', 'proposed_lead_time', 'notes')
    job_spec_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='jobSpecId')
    cost = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='cost')
    currency = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='currency')
    material_id = sgqlc.types.Field(ID, graphql_name='materialId')
    process_id = sgqlc.types.Field(ID, graphql_name='processId')
    manufacturer_id = sgqlc.types.Field(ID, graphql_name='manufacturerId')
    valid_until = sgqlc.types.Field(Time, graphql_name='validUntil')
    is_shipping_included = sgqlc.types.Field(Boolean, graphql_name='isShippingIncluded')
    is_estimated = sgqlc.types.Field(Boolean, graphql_name='isEstimated')
    proposed_lead_time = sgqlc.types.Field(Time, graphql_name='proposedLeadTime')
    notes = sgqlc.types.Field(String, graphql_name='notes')


class CreateRequestForQuotesInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('job_spec', 'type', 'manufacturer_ids', 'quoting_priority', 'quoting_priority_description', 'quotes_needed_by', 'estimated_award_date')
    job_spec = sgqlc.types.Field(sgqlc.types.non_null(CreateJobSpecInput), graphql_name='jobSpec')
    type = sgqlc.types.Field(sgqlc.types.non_null(RequestForQuoteType), graphql_name='type')
    manufacturer_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='manufacturerIds')
    quoting_priority = sgqlc.types.Field(QuotingPriority, graphql_name='quotingPriority')
    quoting_priority_description = sgqlc.types.Field(String, graphql_name='quotingPriorityDescription')
    quotes_needed_by = sgqlc.types.Field(Time, graphql_name='quotesNeededBy')
    estimated_award_date = sgqlc.types.Field(Time, graphql_name='estimatedAwardDate')


class CreateSelectionOptionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'for_id', 'value_type', 'order', 'nil_label', 'required', 'unit', 'prefix')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    for_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='forId')
    value_type = sgqlc.types.Field(sgqlc.types.non_null(OptionValueType), graphql_name='valueType')
    order = sgqlc.types.Field(String, graphql_name='order')
    nil_label = sgqlc.types.Field(String, graphql_name='nilLabel')
    required = sgqlc.types.Field(Boolean, graphql_name='required')
    unit = sgqlc.types.Field(String, graphql_name='unit')
    prefix = sgqlc.types.Field(String, graphql_name='prefix')


class CreateServiceInstancesInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('process_id', 'material_ids', 'manufacturer_id')
    process_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='processId')
    material_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='materialIds')
    manufacturer_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='manufacturerId')


class CreateSharedFileInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('file_id', 'target_space_slug', 'private')
    file_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='fileId')
    target_space_slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='targetSpaceSlug')
    private = sgqlc.types.Field(Boolean, graphql_name='private')


class DeleteAddressInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('address_id',)
    address_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='addressId')


class DeleteAnnotationInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('annotation_id',)
    annotation_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='annotationId')


class DeleteInviteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('invite_id',)
    invite_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='inviteId')


class DeleteInviteLinkInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('invite_link_id',)
    invite_link_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='inviteLinkId')


class DeleteMessageInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('message_id',)
    message_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='messageId')


class DeletePaymentMethodInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space_slug', 'card_id')
    space_slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='spaceSlug')
    card_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='cardId')


class DeleteSharedFileInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class FileInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'space_id', 'filename', 'content_type', 'size', 'git_hash', 'file_last_modified', 'completed', 'cancelled', 'private', 'project_path')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    space_id = sgqlc.types.Field(ID, graphql_name='spaceId')
    filename = sgqlc.types.Field(String, graphql_name='filename')
    content_type = sgqlc.types.Field(String, graphql_name='contentType')
    size = sgqlc.types.Field(Int, graphql_name='size')
    git_hash = sgqlc.types.Field(String, graphql_name='gitHash')
    file_last_modified = sgqlc.types.Field(DateTime, graphql_name='fileLastModified')
    completed = sgqlc.types.Field(Boolean, graphql_name='completed')
    cancelled = sgqlc.types.Field(Boolean, graphql_name='cancelled')
    private = sgqlc.types.Field(Boolean, graphql_name='private')
    project_path = sgqlc.types.Field(String, graphql_name='projectPath')


class FilterInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('field', 'values', 'operator')
    field = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='field')
    values = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ValueInput'))), graphql_name='values')
    operator = sgqlc.types.Field(sgqlc.types.non_null(Operator), graphql_name='operator')


class FollowInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('content_id', 'follow')
    content_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentId')
    follow = sgqlc.types.Field(Boolean, graphql_name='follow')


class ForkProjectInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('project_id', 'target_space_slug', 'name')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='projectId')
    target_space_slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='targetSpaceSlug')
    name = sgqlc.types.Field(String, graphql_name='name')


class ForumInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space_id', 'description')
    space_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='spaceId')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')


class GeolocationInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('longitude', 'latitude')
    longitude = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='longitude')
    latitude = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='latitude')


class GetAddressesInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space_id', 'default')
    space_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='spaceId')
    default = sgqlc.types.Field(Boolean, graphql_name='default')


class GetAnnotationsInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('context_id', 'resource_id')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    resource_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='resourceId')


class GetAssembliesInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('file_id',)
    file_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='fileId')


class GetMessagesInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('context_id', 'resource_id', 'reference_id', 'message_type')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    resource_id = sgqlc.types.Field(String, graphql_name='resourceId')
    reference_id = sgqlc.types.Field(String, graphql_name='referenceId')
    message_type = sgqlc.types.Field(String, graphql_name='messageType')


class ImportProjectInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space', 'name', 'private', 'import_url', 'import_token')
    space = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='space')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    private = sgqlc.types.Field(Boolean, graphql_name='private')
    import_url = sgqlc.types.Field(sgqlc.types.non_null(ImportUrlString), graphql_name='importUrl')
    import_token = sgqlc.types.Field(String, graphql_name='importToken')


class InitiativeInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'title', 'slug', 'avatar', 'description', 'organization_type_id', 'tags', 'social_accounts', 'invites', 'start_free_trial')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    title = sgqlc.types.Field(String, graphql_name='title')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    avatar = sgqlc.types.Field(String, graphql_name='avatar')
    description = sgqlc.types.Field(String, graphql_name='description')
    organization_type_id = sgqlc.types.Field(ID, graphql_name='organizationTypeId')
    tags = sgqlc.types.Field(sgqlc.types.list_of('TagInput'), graphql_name='tags')
    social_accounts = sgqlc.types.Field(sgqlc.types.list_of('SocialAccountInput'), graphql_name='socialAccounts')
    invites = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='invites')
    start_free_trial = sgqlc.types.Field(Boolean, graphql_name='startFreeTrial')


class InvitesRequestInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('msg',)
    msg = sgqlc.types.Field(String, graphql_name='msg')


class IssueAssigneeInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('profile_id', 'deleted')
    profile_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='profileId')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')


class IssueInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'project_id', 'title', 'description', 'status', 'labels', 'assignees', 'tags')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    project_id = sgqlc.types.Field(ID, graphql_name='projectId')
    title = sgqlc.types.Field(String, graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    status = sgqlc.types.Field(String, graphql_name='status')
    labels = sgqlc.types.Field(sgqlc.types.list_of('IssueLabelInput'), graphql_name='labels')
    assignees = sgqlc.types.Field(sgqlc.types.list_of(IssueAssigneeInput), graphql_name='assignees')
    tags = sgqlc.types.Field(sgqlc.types.list_of('TagInput'), graphql_name='tags')


class IssueLabelInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('label_id', 'deleted')
    label_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='labelId')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')


class LabelInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'project_id', 'name', 'color', 'restricted')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    project_id = sgqlc.types.Field(ID, graphql_name='projectId')
    name = sgqlc.types.Field(String, graphql_name='name')
    color = sgqlc.types.Field(String, graphql_name='color')
    restricted = sgqlc.types.Field(Boolean, graphql_name='restricted')


class LikeInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('content_id', 'like')
    content_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentId')
    like = sgqlc.types.Field(Boolean, graphql_name='like')


class MakeDefaultPaymentMethodInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space_slug', 'card_id')
    space_slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='spaceSlug')
    card_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='cardId')


class ManufacturerFilter(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('manufacturer_ids', 'pattern', 'materials', 'processes', 'ships_to', 'company_type')
    manufacturer_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='manufacturerIds')
    pattern = sgqlc.types.Field(String, graphql_name='pattern')
    materials = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='materials')
    processes = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='processes')
    ships_to = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='shipsTo')
    company_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='companyType')


class ManufacturerInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('enquiry_email', 'address', 'ships_to', 'telephone', 'founding_year', 'avatar_id', 'geolocation', 'industries', 'num_employees', 'num_machines', 'minimum_order_quantity', 'lead_time', 'file_formats', 'case_studies', 'company_type')
    enquiry_email = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='enquiryEmail')
    address = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='address')
    ships_to = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='shipsTo')
    telephone = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='telephone')
    founding_year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='foundingYear')
    avatar_id = sgqlc.types.Field(String, graphql_name='avatarId')
    geolocation = sgqlc.types.Field(GeolocationInput, graphql_name='geolocation')
    industries = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='industries')
    num_employees = sgqlc.types.Field(Int, graphql_name='numEmployees')
    num_machines = sgqlc.types.Field(Int, graphql_name='numMachines')
    minimum_order_quantity = sgqlc.types.Field(Int, graphql_name='minimumOrderQuantity')
    lead_time = sgqlc.types.Field(String, graphql_name='leadTime')
    file_formats = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='fileFormats')
    case_studies = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='caseStudies')
    company_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='companyType')


class MaterialFilter(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('process_id', 'name')
    process_id = sgqlc.types.Field(ID, graphql_name='processId')
    name = sgqlc.types.Field(String, graphql_name='name')


class MaterialInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'is_selectable', 'children')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    is_selectable = sgqlc.types.Field(Boolean, graphql_name='isSelectable')
    children = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('MaterialInput')), graphql_name='children')


class MoveGroupInviteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('invite_id', 'group_id')
    invite_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='inviteId')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='groupId')


class MoveGroupMemberInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space_id', 'user_id', 'group_id')
    space_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='spaceId')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='userId')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='groupId')


class NewPasswordInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('username', 'expiry_time', 'hmac', 'new_password')
    username = sgqlc.types.Field(String, graphql_name='username')
    expiry_time = sgqlc.types.Field(String, graphql_name='expiryTime')
    hmac = sgqlc.types.Field(String, graphql_name='hmac')
    new_password = sgqlc.types.Field(String, graphql_name='newPassword')


class OperationInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('project_id', 'op_type', 'file_id', 'path', 'old_path')
    project_id = sgqlc.types.Field(ID, graphql_name='projectId')
    op_type = sgqlc.types.Field(String, graphql_name='opType')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    path = sgqlc.types.Field(String, graphql_name='path')
    old_path = sgqlc.types.Field(String, graphql_name='oldPath')


class OptionFilter(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('material_id', 'process_id', 'selected_option_instance')
    material_id = sgqlc.types.Field(ID, graphql_name='materialId')
    process_id = sgqlc.types.Field(ID, graphql_name='processId')
    selected_option_instance = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('SelectedOptionValueInput')), graphql_name='selectedOptionInstance')


class OptionInstanceFilter(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('option_id', 'material_id', 'process_id')
    option_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='optionId')
    material_id = sgqlc.types.Field(ID, graphql_name='materialId')
    process_id = sgqlc.types.Field(ID, graphql_name='processId')


class PinInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('category_id', 'thread_id', 'pin')
    category_id = sgqlc.types.Field(ID, graphql_name='categoryId')
    thread_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='threadId')
    pin = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='pin')


class PostInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'title', 'msg', 'url', 'tags', 'upvote')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    title = sgqlc.types.Field(String, graphql_name='title')
    msg = sgqlc.types.Field(String, graphql_name='msg')
    url = sgqlc.types.Field(String, graphql_name='url')
    tags = sgqlc.types.Field(sgqlc.types.list_of('TagInput'), graphql_name='tags')
    upvote = sgqlc.types.Field(Boolean, graphql_name='upvote')


class ProcessFilter(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('material_id', 'name')
    material_id = sgqlc.types.Field(ID, graphql_name='materialId')
    name = sgqlc.types.Field(String, graphql_name='name')


class ProcessInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'is_selectable', 'children')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    is_selectable = sgqlc.types.Field(Boolean, graphql_name='isSelectable')
    children = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ProcessInput')), graphql_name='children')


class ProfileInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'username', 'full_name', 'bio', 'avatar', 'skills', 'social_accounts', 'intent_id', 'user_type_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    username = sgqlc.types.Field(String, graphql_name='username')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    avatar = sgqlc.types.Field(ID, graphql_name='avatar')
    skills = sgqlc.types.Field(sgqlc.types.list_of('TagInput'), graphql_name='skills')
    social_accounts = sgqlc.types.Field(sgqlc.types.list_of('SocialAccountInput'), graphql_name='socialAccounts')
    intent_id = sgqlc.types.Field(ID, graphql_name='intentId')
    user_type_id = sgqlc.types.Field(ID, graphql_name='userTypeId')


class ProjectInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'space_id', 'name', 'image', 'description', 'license', 'phase_id', 'tags', 'private', 'invites', 'add_featured', 'remove_featured')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    space_id = sgqlc.types.Field(ID, graphql_name='spaceId')
    name = sgqlc.types.Field(String, graphql_name='name')
    image = sgqlc.types.Field(String, graphql_name='image')
    description = sgqlc.types.Field(String, graphql_name='description')
    license = sgqlc.types.Field(String, graphql_name='license')
    phase_id = sgqlc.types.Field(ID, graphql_name='phaseId')
    tags = sgqlc.types.Field(sgqlc.types.list_of('TagInput'), graphql_name='tags')
    private = sgqlc.types.Field(Boolean, graphql_name='private')
    invites = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='invites')
    add_featured = sgqlc.types.Field(String, graphql_name='addFeatured')
    remove_featured = sgqlc.types.Field(String, graphql_name='removeFeatured')


class ProjectVisibilityInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'space', 'slug', 'private')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    space = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='space')
    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='slug')
    private = sgqlc.types.Field(Boolean, graphql_name='private')


class RejectInviteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('invite_id',)
    invite_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='inviteId')


class RejectQuoteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('quote_id', 'reason', 'description')
    quote_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='quoteId')
    reason = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='reason')
    description = sgqlc.types.Field(String, graphql_name='description')


class ResendInviteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('invite_id',)
    invite_id = sgqlc.types.Field(String, graphql_name='inviteId')


class ResetContributionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('project_id', 'path')
    project_id = sgqlc.types.Field(ID, graphql_name='projectId')
    path = sgqlc.types.Field(String, graphql_name='path')


class SelectedOptionValueInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('selected_value',)
    selected_value = sgqlc.types.Field('SelectedValueInput', graphql_name='selectedValue')


class SelectedValueInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('option_id', 'value_bool', 'value_string', 'value_float', 'value_int')
    option_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='optionId')
    value_bool = sgqlc.types.Field(Boolean, graphql_name='valueBool')
    value_string = sgqlc.types.Field(String, graphql_name='valueString')
    value_float = sgqlc.types.Field(Float, graphql_name='valueFloat')
    value_int = sgqlc.types.Field(Int, graphql_name='valueInt')


class ServiceFilter(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('manufacturer_id', 'material_id', 'process_id')
    manufacturer_id = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='manufacturerId')
    material_id = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='materialId')
    process_id = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='processId')


class SessionFilterInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'request_for_quote_id', 'state')
    id = sgqlc.types.Field(ID, graphql_name='id')
    request_for_quote_id = sgqlc.types.Field(ID, graphql_name='requestForQuoteId')
    state = sgqlc.types.Field(SessionState, graphql_name='state')


class ShippingInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('provider', 'address_id')
    provider = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='provider')
    address_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='addressId')


class SignInInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('username', 'email', 'password', 'sign_out')
    username = sgqlc.types.Field(String, graphql_name='username')
    email = sgqlc.types.Field(String, graphql_name='email')
    password = sgqlc.types.Field(String, graphql_name='password')
    sign_out = sgqlc.types.Field(Boolean, graphql_name='signOut')


class SignupInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('username', 'email', 'password', 'full_name', 'preferred_name', 'locale', 'emails_enabled', 'bio', 'intent_id', 'user_type_id', 'skills', 'start_free_trial', 'encoded_extra')
    username = sgqlc.types.Field(String, graphql_name='username')
    email = sgqlc.types.Field(String, graphql_name='email')
    password = sgqlc.types.Field(String, graphql_name='password')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    preferred_name = sgqlc.types.Field(String, graphql_name='preferredName')
    locale = sgqlc.types.Field(String, graphql_name='locale')
    emails_enabled = sgqlc.types.Field(Boolean, graphql_name='emailsEnabled')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    intent_id = sgqlc.types.Field(ID, graphql_name='intentId')
    user_type_id = sgqlc.types.Field(ID, graphql_name='userTypeId')
    skills = sgqlc.types.Field(sgqlc.types.list_of('TagInput'), graphql_name='skills')
    start_free_trial = sgqlc.types.Field(Boolean, graphql_name='startFreeTrial')
    encoded_extra = sgqlc.types.Field(String, graphql_name='encodedExtra')


class SignupInviteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('emails',)
    emails = sgqlc.types.Field(String, graphql_name='emails')


class SignupRequestInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('email', 'bio')
    email = sgqlc.types.Field(String, graphql_name='email')
    bio = sgqlc.types.Field(String, graphql_name='bio')


class SlugInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('type', 'space', 'text')
    type = sgqlc.types.Field(String, graphql_name='type')
    space = sgqlc.types.Field(ID, graphql_name='space')
    text = sgqlc.types.Field(String, graphql_name='text')


class SocialAccountInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'account_name', 'account_type')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    account_name = sgqlc.types.Field(String, graphql_name='accountName')
    account_type = sgqlc.types.Field(String, graphql_name='accountType')


class StoryInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'space_id', 'title', 'body', 'tags', 'avatar', 'add_featured', 'remove_featured')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    space_id = sgqlc.types.Field(ID, graphql_name='spaceId')
    title = sgqlc.types.Field(String, graphql_name='title')
    body = sgqlc.types.Field(String, graphql_name='body')
    tags = sgqlc.types.Field(sgqlc.types.list_of('TagInput'), graphql_name='tags')
    avatar = sgqlc.types.Field(String, graphql_name='avatar')
    add_featured = sgqlc.types.Field(String, graphql_name='addFeatured')
    remove_featured = sgqlc.types.Field(String, graphql_name='removeFeatured')


class TagInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'deleted', 'name')
    id = sgqlc.types.Field(ID, graphql_name='id')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    name = sgqlc.types.Field(String, graphql_name='name')


class TargetInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('target_type', 'sel_type', 'instance_ix', 'brep_ix', 'body_ix', 'prc_path', 'face_hit', 'face_ix', 'loop_ix', 'edge_ix', 'point_hit', 'point_ix', 'triangle_ix', 'triangle_pt', 'triangle_nr')
    target_type = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='targetType')
    sel_type = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='selType')
    instance_ix = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='instanceIx')
    brep_ix = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='brepIx')
    body_ix = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='bodyIx')
    prc_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='prcPath')
    face_hit = sgqlc.types.Field(Boolean, graphql_name='faceHit')
    face_ix = sgqlc.types.Field(Int, graphql_name='faceIx')
    loop_ix = sgqlc.types.Field(Int, graphql_name='loopIx')
    edge_ix = sgqlc.types.Field(Int, graphql_name='edgeIx')
    point_hit = sgqlc.types.Field(Boolean, graphql_name='pointHit')
    point_ix = sgqlc.types.Field(Int, graphql_name='pointIx')
    triangle_ix = sgqlc.types.Field(Int, graphql_name='triangleIx')
    triangle_pt = sgqlc.types.Field('VectorInput', graphql_name='trianglePt')
    triangle_nr = sgqlc.types.Field('VectorInput', graphql_name='triangleNr')


class ThreadInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'members_only', 'deleted', 'title', 'msg', 'category_id', 'tags')
    id = sgqlc.types.Field(ID, graphql_name='id')
    members_only = sgqlc.types.Field(Boolean, graphql_name='membersOnly')
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    title = sgqlc.types.Field(String, graphql_name='title')
    msg = sgqlc.types.Field(String, graphql_name='msg')
    category_id = sgqlc.types.Field(ID, graphql_name='categoryId')
    tags = sgqlc.types.Field(sgqlc.types.list_of(TagInput), graphql_name='tags')


class TransferProjectInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('space', 'slug', 'target_space')
    space = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='space')
    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='slug')
    target_space = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='targetSpace')


class UpdateAddressInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('address_id', 'default')
    address_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='addressId')
    default = sgqlc.types.Field(Boolean, graphql_name='default')


class UpdateBuildInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('material_id', 'process_id')
    material_id = sgqlc.types.Field(ID, graphql_name='materialId')
    process_id = sgqlc.types.Field(ID, graphql_name='processId')


class UpdateImportProjectInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('project_id', 'import_url', 'import_token')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='projectId')
    import_url = sgqlc.types.Field(ImportUrlString, graphql_name='importUrl')
    import_token = sgqlc.types.Field(String, graphql_name='importToken')


class UpdateJobSpecInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('job_spec_id', 'quantity', 'shipping_address', 'update_build_input')
    job_spec_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='jobSpecId')
    quantity = sgqlc.types.Field(Int, graphql_name='quantity')
    shipping_address = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='shippingAddress')
    update_build_input = sgqlc.types.Field(UpdateBuildInput, graphql_name='updateBuildInput')


class UpdateManufacturerInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('manufacturing_id', 'enquiry_email', 'ships_to', 'telephone', 'founding_year', 'industries', 'num_employees', 'num_machines', 'file_formats', 'case_studies', 'company_type')
    manufacturing_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='manufacturingId')
    enquiry_email = sgqlc.types.Field(String, graphql_name='enquiryEmail')
    ships_to = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='shipsTo')
    telephone = sgqlc.types.Field(String, graphql_name='telephone')
    founding_year = sgqlc.types.Field(Int, graphql_name='foundingYear')
    industries = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='industries')
    num_employees = sgqlc.types.Field(Int, graphql_name='numEmployees')
    num_machines = sgqlc.types.Field(Int, graphql_name='numMachines')
    file_formats = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='fileFormats')
    case_studies = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='caseStudies')
    company_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='companyType')


class UpdateMessageInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('message_id', 'body')
    message_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='messageId')
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='body')


class UpdateOptionInstanceInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('option_instance_id', 'option_id', 'value_int', 'value_float', 'value_string', 'value_bool')
    option_instance_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='optionInstanceId')
    option_id = sgqlc.types.Field(ID, graphql_name='optionId')
    value_int = sgqlc.types.Field(Int, graphql_name='valueInt')
    value_float = sgqlc.types.Field(Float, graphql_name='valueFloat')
    value_string = sgqlc.types.Field(String, graphql_name='valueString')
    value_bool = sgqlc.types.Field(Boolean, graphql_name='valueBool')


class UpdateOrderInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('order_id', 'order_status')
    order_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='orderId')
    order_status = sgqlc.types.Field(sgqlc.types.non_null(OrderStatus), graphql_name='orderStatus')


class UpdateRequestForQuoteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('request_for_quote_id', 'quotes_needed_by', 'estimated_award_date', 'update_job_spec_input')
    request_for_quote_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='requestForQuoteId')
    quotes_needed_by = sgqlc.types.Field(Time, graphql_name='quotesNeededBy')
    estimated_award_date = sgqlc.types.Field(Time, graphql_name='estimatedAwardDate')
    update_job_spec_input = sgqlc.types.Field(UpdateJobSpecInput, graphql_name='updateJobSpecInput')


class UpdateServiceInstanceInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('service_instance_id', 'is_archived')
    service_instance_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='serviceInstanceId')
    is_archived = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isArchived')


class UpdateSharedFileInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'file_id', 'private')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    private = sgqlc.types.Field(Boolean, graphql_name='private')


class UserGroupActionInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('username', 'space_id', 'group_name')
    username = sgqlc.types.Field(String, graphql_name='username')
    space_id = sgqlc.types.Field(String, graphql_name='spaceId')
    group_name = sgqlc.types.Field(String, graphql_name='groupName')


class UserGroupInviteInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('invites', 'space_id', 'group_name')
    invites = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='invites')
    space_id = sgqlc.types.Field(String, graphql_name='spaceId')
    group_name = sgqlc.types.Field(String, graphql_name='groupName')


class ValueInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('value_string', 'value_int', 'value_float', 'value_bool', 'value_date_time', 'value_type')
    value_string = sgqlc.types.Field(String, graphql_name='valueString')
    value_int = sgqlc.types.Field(Int, graphql_name='valueInt')
    value_float = sgqlc.types.Field(Float, graphql_name='valueFloat')
    value_bool = sgqlc.types.Field(Boolean, graphql_name='valueBool')
    value_date_time = sgqlc.types.Field(Time, graphql_name='valueDateTime')
    value_type = sgqlc.types.Field(sgqlc.types.non_null(ValueInputType), graphql_name='valueType')


class VectorInput(sgqlc.types.Input):
    __schema__ = WIF_schema
    __field_names__ = ('x', 'y', 'z')
    x = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='x')
    y = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='y')
    z = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='z')



########################################################################
# Output Objects and Interfaces
########################################################################
class AcceptInvite(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class ActivityConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('ActivityEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class ActivityEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('ActivityFeedLine', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ActivityFeedLine(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'action', 'date', 'origin', 'content')
    id = sgqlc.types.Field(ID, graphql_name='id')
    action = sgqlc.types.Field(String, graphql_name='action')
    date = sgqlc.types.Field(DateTime, graphql_name='date')
    origin = sgqlc.types.Field('ActivityOrigin', graphql_name='origin')
    content = sgqlc.types.Field('ActivityContent', graphql_name='content')


class AddPaymentMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'payment_method')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    payment_method = sgqlc.types.Field('CreditCard', graphql_name='paymentMethod')


class Annotation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'context_id', 'resource_id', 'body', 'created_by', 'target', 'timestamp', 'camera', 'hoops_version', 'import_config', 'temp_key')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextId')
    resource_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='resourceId')
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='body')
    created_by = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='createdBy')
    target = sgqlc.types.Field(sgqlc.types.non_null('Target'), graphql_name='target')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='timestamp')
    camera = sgqlc.types.Field(sgqlc.types.non_null('Camera'), graphql_name='camera')
    hoops_version = sgqlc.types.Field(String, graphql_name='hoopsVersion')
    import_config = sgqlc.types.Field(String, graphql_name='importConfig')
    temp_key = sgqlc.types.Field(String, graphql_name='tempKey')


class AutoBillingInvoiceConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('AutoBillingInvoiceEdge')), graphql_name='edges')


class AutoBillingInvoiceEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('BillingInvoice', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class AutoGroupConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('AutoGroupEdge')), graphql_name='edges')


class AutoGroupEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Group', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class AutoGroupInviteConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('AutoGroupInviteEdge')), graphql_name='edges')


class AutoGroupInviteEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('GroupInvite', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class AutoInviteLinkConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('AutoInviteLinkEdge')), graphql_name='edges')


class AutoInviteLinkEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('InviteLink', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class BanProfile(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'management')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    management = sgqlc.types.Field(JSONString, graphql_name='management')


class BillingAddSeatsMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'subscription')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    subscription = sgqlc.types.Field('BillingSubscription', graphql_name='subscription')


class BillingCancelSubscriptionMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'subscription')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    subscription = sgqlc.types.Field('BillingSubscription', graphql_name='subscription')


class BillingRemoveSeatsMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'subscription')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    subscription = sgqlc.types.Field('BillingSubscription', graphql_name='subscription')


class BillingSubscribeMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'subscription')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    subscription = sgqlc.types.Field('BillingSubscription', graphql_name='subscription')


class BuildValue(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('of', 'value_float', 'value_int', 'value_string', 'value_bool')
    of = sgqlc.types.Field(sgqlc.types.non_null('Option'), graphql_name='of')
    value_float = sgqlc.types.Field(Float, graphql_name='valueFloat')
    value_int = sgqlc.types.Field(Int, graphql_name='valueInt')
    value_string = sgqlc.types.Field(String, graphql_name='valueString')
    value_bool = sgqlc.types.Field(Boolean, graphql_name='valueBool')


class Camera(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('up', 'right', 'position', 'lookat')
    up = sgqlc.types.Field(sgqlc.types.non_null('Vector'), graphql_name='up')
    right = sgqlc.types.Field(sgqlc.types.non_null('Vector'), graphql_name='right')
    position = sgqlc.types.Field(sgqlc.types.non_null('Vector'), graphql_name='position')
    lookat = sgqlc.types.Field(sgqlc.types.non_null('Vector'), graphql_name='lookat')


class CancelImportProjectMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class CategoryMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'category')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    category = sgqlc.types.Field('Category', graphql_name='category')


class ChangeEmailPreferences(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'msg')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    msg = sgqlc.types.Field(String, graphql_name='msg')


class ChangeLanguagePreferences(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'msg')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    msg = sgqlc.types.Field(String, graphql_name='msg')


class ChangePassword(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'msg')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    msg = sgqlc.types.Field(String, graphql_name='msg')


class ChannelConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('ChannelEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class ChannelConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(ChannelConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class ChannelEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Channel', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class CollectionConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('CollectionEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class CollectionConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(CollectionConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class CollectionEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Collection', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class CollectionMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'collection', 'project')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    collection = sgqlc.types.Field('Collection', graphql_name='collection')
    project = sgqlc.types.Field('Project', graphql_name='project')


class CommentConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('CommentEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class CommentEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Comment', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class CommentMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'comment')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    comment = sgqlc.types.Field('Comment', graphql_name='comment')


class CommitMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'project', 'conflicts', 'conflicts_parent')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    project = sgqlc.types.Field('Project', graphql_name='project')
    conflicts = sgqlc.types.Field(sgqlc.types.list_of('Conflict'), graphql_name='conflicts')
    conflicts_parent = sgqlc.types.Field(String, graphql_name='conflictsParent')


class ConfirmProfile(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'profile')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    profile = sgqlc.types.Field('Profile', graphql_name='profile')


class Confirmation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'customer', 'timestamp')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    customer = sgqlc.types.Field(String, graphql_name='customer')
    timestamp = sgqlc.types.Field(Time, graphql_name='timestamp')


class Conflict(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'path', 'local', 'local_status', 'remote', 'remote_contribution', 'remote_status')
    id = sgqlc.types.Field(String, graphql_name='id')
    path = sgqlc.types.Field(String, graphql_name='path')
    local = sgqlc.types.Field('File', graphql_name='local')
    local_status = sgqlc.types.Field(Status, graphql_name='localStatus')
    remote = sgqlc.types.Field('File', graphql_name='remote')
    remote_contribution = sgqlc.types.Field('Contribution', graphql_name='remoteContribution')
    remote_status = sgqlc.types.Field(Status, graphql_name='remoteStatus')


class ContentInterface(sgqlc.types.Interface):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'content_type', 'slug', 'space', 'parent_slug', 'is_private', 'description', 'whitelabel', 'creator', 'date_created', 'last_updated', 'likes_count', 'followers_count', 'comments_count', 'snippet')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    content_type = sgqlc.types.Field(String, graphql_name='contentType')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    space = sgqlc.types.Field('Space', graphql_name='space')
    parent_slug = sgqlc.types.Field(String, graphql_name='parentSlug')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    description = sgqlc.types.Field(String, graphql_name='description')
    whitelabel = sgqlc.types.Field(String, graphql_name='whitelabel')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    likes_count = sgqlc.types.Field(Int, graphql_name='likesCount')
    followers_count = sgqlc.types.Field(Int, graphql_name='followersCount')
    comments_count = sgqlc.types.Field(Int, graphql_name='commentsCount')
    snippet = sgqlc.types.Field(String, graphql_name='snippet')


class ContributionConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('ContributionEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class ContributionEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Contribution', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ConversionMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'conversion')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    conversion = sgqlc.types.Field('FileConversion', graphql_name='conversion')


class CreateInviteLink(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'invite_link')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    invite_link = sgqlc.types.Field('InviteLink', graphql_name='inviteLink')


class CreateSharedFileMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'shared_file')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    shared_file = sgqlc.types.Field('SharedFile', graphql_name='sharedFile')


class DeleteInvite(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'group')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    group = sgqlc.types.Field('Group', graphql_name='group')


class DeleteInviteLink(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class DeletePaymentMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors',)
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')


class DeleteSharedFileMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class DiffInfo(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('project', 'contributions_ahead', 'contributions_behind')
    project = sgqlc.types.Field('Project', graphql_name='project')
    contributions_ahead = sgqlc.types.Field(Int, graphql_name='contributionsAhead')
    contributions_behind = sgqlc.types.Field(Int, graphql_name='contributionsBehind')


class EmailLogin(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'username', 'profile')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    username = sgqlc.types.Field(String, graphql_name='username')
    profile = sgqlc.types.Field('Profile', graphql_name='profile')


class EmailSignup(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'profile')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    profile = sgqlc.types.Field('Profile', graphql_name='profile')


class EmailType(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'description', 'display_name', 'enabled')
    id = sgqlc.types.Field(ID, graphql_name='id')
    description = sgqlc.types.Field(String, graphql_name='description')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')


class FileMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'file')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    file = sgqlc.types.Field('File', graphql_name='file')


class FollowMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'content')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    content = sgqlc.types.Field('Content', graphql_name='content')


class ForkProjectMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'project')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    project = sgqlc.types.Field('Project', graphql_name='project')


class ForumConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('ForumEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class ForumConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(ForumConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class ForumEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Forum', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ForumMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'forum')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    forum = sgqlc.types.Field('Forum', graphql_name='forum')


class GroupMember(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('group_id', 'user_id', 'intrinsic', 'invite_link_id', 'group', 'invite_link', 'can_update', 'can_delete', 'id', 'profile')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='groupId')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='userId')
    intrinsic = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='intrinsic')
    invite_link_id = sgqlc.types.Field(Int, graphql_name='inviteLinkId')
    group = sgqlc.types.Field('Group', graphql_name='group')
    invite_link = sgqlc.types.Field('InviteLink', graphql_name='inviteLink')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    id = sgqlc.types.Field(ID, graphql_name='id')
    profile = sgqlc.types.Field('Profile', graphql_name='profile')


class HTMLNotification(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'html', 'url', 'level')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    html = sgqlc.types.Field(String, graphql_name='html')
    url = sgqlc.types.Field(String, graphql_name='url')
    level = sgqlc.types.Field(String, graphql_name='level')


class ImportProjectMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'project')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    project = sgqlc.types.Field('Project', graphql_name='project')


class ImportStatus(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('general_progress', 'status_progress', 'status', 'import_service')
    general_progress = sgqlc.types.Field(Float, graphql_name='generalProgress')
    status_progress = sgqlc.types.Field(Float, graphql_name='statusProgress')
    status = sgqlc.types.Field(String, graphql_name='status')
    import_service = sgqlc.types.Field(String, graphql_name='importService')


class InitiativeConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('InitiativeEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class InitiativeConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(InitiativeConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class InitiativeEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Initiative', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class InitiativeMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'initiative')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    initiative = sgqlc.types.Field('Initiative', graphql_name='initiative')


class InitiativeProfileMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'initiative', 'profile')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    initiative = sgqlc.types.Field('Initiative', graphql_name='initiative')
    profile = sgqlc.types.Field('Profile', graphql_name='profile')


class InviteUsersToGroup(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'group')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    group = sgqlc.types.Field('Group', graphql_name='group')


class InviteUsersToSignup(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'invites', 'invites_left')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    invites = sgqlc.types.Field(sgqlc.types.list_of('GroupInvite'), graphql_name='invites')
    invites_left = sgqlc.types.Field(Int, graphql_name='invitesLeft')


class InvitesRequest(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class IssueConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('IssueEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class IssueConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(IssueConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class IssueEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Issue', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class IssueMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'issue')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    issue = sgqlc.types.Field('Issue', graphql_name='issue')


class LabelMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'label')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    label = sgqlc.types.Field('Label', graphql_name='label')


class License(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'title', 'link', 'is_header', 'abreviation')
    name = sgqlc.types.Field(String, graphql_name='name')
    title = sgqlc.types.Field(String, graphql_name='title')
    link = sgqlc.types.Field(String, graphql_name='link')
    is_header = sgqlc.types.Field(Boolean, graphql_name='isHeader')
    abreviation = sgqlc.types.Field(String, graphql_name='abreviation')


class LikeMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'content')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    content = sgqlc.types.Field('Content', graphql_name='content')


class MakeDefaultPaymentMethodMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'payment_method')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    payment_method = sgqlc.types.Field('CreditCard', graphql_name='paymentMethod')


class ManufacturerInitiativeProfileMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'initiative', 'profile')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    initiative = sgqlc.types.Field('Initiative', graphql_name='initiative')
    profile = sgqlc.types.Field('Profile', graphql_name='profile')


class MarkAllAsReadMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'pending_count', 'marked_as_read_count')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    pending_count = sgqlc.types.Field(Int, graphql_name='pendingCount')
    marked_as_read_count = sgqlc.types.Field(Int, graphql_name='markedAsReadCount')


class MoveGroupInvite(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'from_group', 'to_group')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    from_group = sgqlc.types.Field('Group', graphql_name='fromGroup')
    to_group = sgqlc.types.Field('Group', graphql_name='toGroup')


class MoveGroupMember(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'from_group', 'to_group')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    from_group = sgqlc.types.Field('Group', graphql_name='fromGroup')
    to_group = sgqlc.types.Field('Group', graphql_name='toGroup')


class Mutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('signup_result', 'sign_in_result', 'profile', 'confirm_profile', 'ban_profile', 'initiative', 'initiative_and_profile', 'manufacturer_and_initiative_and_profile', 'post', 'comment', 'story', 'project', 'project_visibility', 'transfer_project', 'import_project', 'cancel_import_project', 'update_import_project', 'fork_project', 'create_shared_file', 'delete_shared_file', 'update_shared_file', 'collection', 'like', 'follow', 'label', 'issue', 'file', 'conversion', 'commit', 'reset_contribution', 'operation', 'request_reset_password', 'new_password', 'change_password', 'change_email_preferences', 'change_language_preferences', 'invite_users_to_group', 'invite_users_to_signup', 'resend_invite', 'remove_user_from_group', 'move_group_member', 'move_group_invite', 'request_more_invites', 'request_invite', 'delete_invite', 'accept_invite', 'reject_invite', 'create_invite_link', 'delete_invite_link', 'forum', 'thread', 'category', 'pin', 'billing_subscribe', 'billing_cancel', 'billing_add_seats', 'billing_remove_seats', 'add_payment_method', 'delete_payment_method', 'make_default_payment_method', 'mark_all_as_read', 'create_annotation', 'delete_annotation', 'create_assembly', 'convert_assembly', 'create_address', 'update_address', 'delete_address', 'create_intermediator', 'create_manufacturer', 'update_manufacturer', 'create_service_instances', 'update_service_instance', 'create_option_instances', 'update_option_instance', 'create_materials', 'create_processes', 'create_min_max_option', 'create_selection_option', 'create_message', 'update_message', 'delete_message', 'create_order', 'update_order', 'confirm_order', 'cancel_order', 'create_request_for_quote', 'close_request_for_quote', 'update_request_for_quote', 'assign_request_for_quote', 'close_session', 'create_quote', 'reject_quote')
    signup_result = sgqlc.types.Field(EmailSignup, graphql_name='signupResult', args=sgqlc.types.ArgDict((
        ('signup_data', sgqlc.types.Arg(SignupInput, graphql_name='signupData', default=None)),
))
    )
    sign_in_result = sgqlc.types.Field(EmailLogin, graphql_name='signInResult', args=sgqlc.types.ArgDict((
        ('sign_in_data', sgqlc.types.Arg(SignInInput, graphql_name='signInData', default=None)),
))
    )
    profile = sgqlc.types.Field('UpdateProfile', graphql_name='profile', args=sgqlc.types.ArgDict((
        ('profile_data', sgqlc.types.Arg(ProfileInput, graphql_name='profileData', default=None)),
))
    )
    confirm_profile = sgqlc.types.Field(ConfirmProfile, graphql_name='confirmProfile', args=sgqlc.types.ArgDict((
        ('profile_data', sgqlc.types.Arg(ConfirmProfileInput, graphql_name='profileData', default=None)),
))
    )
    ban_profile = sgqlc.types.Field(BanProfile, graphql_name='banProfile', args=sgqlc.types.ArgDict((
        ('ban_data', sgqlc.types.Arg(BanProfileInput, graphql_name='banData', default=None)),
))
    )
    initiative = sgqlc.types.Field(InitiativeMutation, graphql_name='initiative', args=sgqlc.types.ArgDict((
        ('initiative_data', sgqlc.types.Arg(InitiativeInput, graphql_name='initiativeData', default=None)),
))
    )
    initiative_and_profile = sgqlc.types.Field(InitiativeProfileMutation, graphql_name='initiativeAndProfile', args=sgqlc.types.ArgDict((
        ('initiative_data', sgqlc.types.Arg(InitiativeInput, graphql_name='initiativeData', default=None)),
        ('profile_data', sgqlc.types.Arg(SignupInput, graphql_name='profileData', default=None)),
))
    )
    manufacturer_and_initiative_and_profile = sgqlc.types.Field(ManufacturerInitiativeProfileMutation, graphql_name='manufacturerAndInitiativeAndProfile', args=sgqlc.types.ArgDict((
        ('initiative_data', sgqlc.types.Arg(sgqlc.types.non_null(InitiativeInput), graphql_name='initiativeData', default=None)),
        ('manufacturer_data', sgqlc.types.Arg(sgqlc.types.non_null(ManufacturerInput), graphql_name='manufacturerData', default=None)),
        ('profile_data', sgqlc.types.Arg(sgqlc.types.non_null(SignupInput), graphql_name='profileData', default=None)),
))
    )
    post = sgqlc.types.Field('PostMutation', graphql_name='post', args=sgqlc.types.ArgDict((
        ('post_data', sgqlc.types.Arg(PostInput, graphql_name='postData', default=None)),
))
    )
    comment = sgqlc.types.Field(CommentMutation, graphql_name='comment', args=sgqlc.types.ArgDict((
        ('comment_data', sgqlc.types.Arg(CommentInput, graphql_name='commentData', default=None)),
))
    )
    story = sgqlc.types.Field('StoryMutation', graphql_name='story', args=sgqlc.types.ArgDict((
        ('story_data', sgqlc.types.Arg(StoryInput, graphql_name='storyData', default=None)),
))
    )
    project = sgqlc.types.Field('ProjectMutation', graphql_name='project', args=sgqlc.types.ArgDict((
        ('project_data', sgqlc.types.Arg(ProjectInput, graphql_name='projectData', default=None)),
))
    )
    project_visibility = sgqlc.types.Field('ProjectVisibilityMutation', graphql_name='projectVisibility', args=sgqlc.types.ArgDict((
        ('project_visibility_input', sgqlc.types.Arg(sgqlc.types.non_null(ProjectVisibilityInput), graphql_name='projectVisibilityInput', default=None)),
))
    )
    transfer_project = sgqlc.types.Field('TransferProjectMutation', graphql_name='transferProject', args=sgqlc.types.ArgDict((
        ('transfer_project_input', sgqlc.types.Arg(sgqlc.types.non_null(TransferProjectInput), graphql_name='transferProjectInput', default=None)),
))
    )
    import_project = sgqlc.types.Field(ImportProjectMutation, graphql_name='importProject', args=sgqlc.types.ArgDict((
        ('import_input', sgqlc.types.Arg(sgqlc.types.non_null(ImportProjectInput), graphql_name='importInput', default=None)),
))
    )
    cancel_import_project = sgqlc.types.Field(CancelImportProjectMutation, graphql_name='cancelImportProject', args=sgqlc.types.ArgDict((
        ('cancel_import_input', sgqlc.types.Arg(sgqlc.types.non_null(CancelImportProjectInput), graphql_name='cancelImportInput', default=None)),
))
    )
    update_import_project = sgqlc.types.Field('UpdateImportProjectMutation', graphql_name='updateImportProject', args=sgqlc.types.ArgDict((
        ('update_import_input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateImportProjectInput), graphql_name='updateImportInput', default=None)),
))
    )
    fork_project = sgqlc.types.Field(ForkProjectMutation, graphql_name='forkProject', args=sgqlc.types.ArgDict((
        ('fork_input', sgqlc.types.Arg(sgqlc.types.non_null(ForkProjectInput), graphql_name='forkInput', default=None)),
))
    )
    create_shared_file = sgqlc.types.Field(CreateSharedFileMutation, graphql_name='createSharedFile', args=sgqlc.types.ArgDict((
        ('create_shared_file_input', sgqlc.types.Arg(sgqlc.types.non_null(CreateSharedFileInput), graphql_name='createSharedFileInput', default=None)),
))
    )
    delete_shared_file = sgqlc.types.Field(DeleteSharedFileMutation, graphql_name='deleteSharedFile', args=sgqlc.types.ArgDict((
        ('delete_shared_file_input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteSharedFileInput), graphql_name='deleteSharedFileInput', default=None)),
))
    )
    update_shared_file = sgqlc.types.Field('UpdateSharedFileMutation', graphql_name='updateSharedFile', args=sgqlc.types.ArgDict((
        ('update_shared_file_input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateSharedFileInput), graphql_name='updateSharedFileInput', default=None)),
))
    )
    collection = sgqlc.types.Field(CollectionMutation, graphql_name='collection', args=sgqlc.types.ArgDict((
        ('collection_data', sgqlc.types.Arg(CollectionInput, graphql_name='collectionData', default=None)),
))
    )
    like = sgqlc.types.Field(LikeMutation, graphql_name='like', args=sgqlc.types.ArgDict((
        ('like_data', sgqlc.types.Arg(LikeInput, graphql_name='likeData', default=None)),
))
    )
    follow = sgqlc.types.Field(FollowMutation, graphql_name='follow', args=sgqlc.types.ArgDict((
        ('follow_data', sgqlc.types.Arg(FollowInput, graphql_name='followData', default=None)),
))
    )
    label = sgqlc.types.Field(LabelMutation, graphql_name='label', args=sgqlc.types.ArgDict((
        ('label_data', sgqlc.types.Arg(LabelInput, graphql_name='labelData', default=None)),
))
    )
    issue = sgqlc.types.Field(IssueMutation, graphql_name='issue', args=sgqlc.types.ArgDict((
        ('issue_data', sgqlc.types.Arg(IssueInput, graphql_name='issueData', default=None)),
))
    )
    file = sgqlc.types.Field(FileMutation, graphql_name='file', args=sgqlc.types.ArgDict((
        ('file_data', sgqlc.types.Arg(FileInput, graphql_name='fileData', default=None)),
))
    )
    conversion = sgqlc.types.Field(ConversionMutation, graphql_name='conversion', args=sgqlc.types.ArgDict((
        ('input_data', sgqlc.types.Arg(ConversionInput, graphql_name='inputData', default=None)),
))
    )
    commit = sgqlc.types.Field(CommitMutation, graphql_name='commit', args=sgqlc.types.ArgDict((
        ('commit_data', sgqlc.types.Arg(CommitInput, graphql_name='commitData', default=None)),
))
    )
    reset_contribution = sgqlc.types.Field('ResetContributionMutation', graphql_name='resetContribution', args=sgqlc.types.ArgDict((
        ('reset_data', sgqlc.types.Arg(ResetContributionInput, graphql_name='resetData', default=None)),
))
    )
    operation = sgqlc.types.Field('OperationMutation', graphql_name='operation', args=sgqlc.types.ArgDict((
        ('operation_data', sgqlc.types.Arg(OperationInput, graphql_name='operationData', default=None)),
))
    )
    request_reset_password = sgqlc.types.Field('RequestResetPassword', graphql_name='requestResetPassword', args=sgqlc.types.ArgDict((
        ('username_or_email', sgqlc.types.Arg(String, graphql_name='usernameOrEmail', default=None)),
))
    )
    new_password = sgqlc.types.Field('NewPassword', graphql_name='newPassword', args=sgqlc.types.ArgDict((
        ('new_password_input', sgqlc.types.Arg(NewPasswordInput, graphql_name='newPasswordInput', default=None)),
))
    )
    change_password = sgqlc.types.Field(ChangePassword, graphql_name='changePassword', args=sgqlc.types.ArgDict((
        ('change_password_input', sgqlc.types.Arg(ChangePasswordInput, graphql_name='changePasswordInput', default=None)),
))
    )
    change_email_preferences = sgqlc.types.Field(ChangeEmailPreferences, graphql_name='changeEmailPreferences', args=sgqlc.types.ArgDict((
        ('change_email_preferences_input', sgqlc.types.Arg(sgqlc.types.list_of(ChangeEmailPreferencesInput), graphql_name='changeEmailPreferencesInput', default=None)),
))
    )
    change_language_preferences = sgqlc.types.Field(ChangeLanguagePreferences, graphql_name='changeLanguagePreferences', args=sgqlc.types.ArgDict((
        ('change_language_preferences_input', sgqlc.types.Arg(ChangeLanguagePreferencesInput, graphql_name='changeLanguagePreferencesInput', default=None)),
))
    )
    invite_users_to_group = sgqlc.types.Field(InviteUsersToGroup, graphql_name='inviteUsersToGroup', args=sgqlc.types.ArgDict((
        ('user_group_input', sgqlc.types.Arg(UserGroupInviteInput, graphql_name='userGroupInput', default=None)),
))
    )
    invite_users_to_signup = sgqlc.types.Field(InviteUsersToSignup, graphql_name='inviteUsersToSignup', args=sgqlc.types.ArgDict((
        ('user_group_input', sgqlc.types.Arg(SignupInviteInput, graphql_name='userGroupInput', default=None)),
))
    )
    resend_invite = sgqlc.types.Field('ResendInvite', graphql_name='resendInvite', args=sgqlc.types.ArgDict((
        ('resend_input', sgqlc.types.Arg(ResendInviteInput, graphql_name='resendInput', default=None)),
))
    )
    remove_user_from_group = sgqlc.types.Field('RemoveUserFromGroup', graphql_name='removeUserFromGroup', args=sgqlc.types.ArgDict((
        ('user_group_input', sgqlc.types.Arg(UserGroupActionInput, graphql_name='userGroupInput', default=None)),
))
    )
    move_group_member = sgqlc.types.Field(MoveGroupMember, graphql_name='moveGroupMember', args=sgqlc.types.ArgDict((
        ('move_group_member_input', sgqlc.types.Arg(MoveGroupMemberInput, graphql_name='moveGroupMemberInput', default=None)),
))
    )
    move_group_invite = sgqlc.types.Field(MoveGroupInvite, graphql_name='moveGroupInvite', args=sgqlc.types.ArgDict((
        ('move_group_invite_input', sgqlc.types.Arg(MoveGroupInviteInput, graphql_name='moveGroupInviteInput', default=None)),
))
    )
    request_more_invites = sgqlc.types.Field(InvitesRequest, graphql_name='requestMoreInvites', args=sgqlc.types.ArgDict((
        ('request_input', sgqlc.types.Arg(InvitesRequestInput, graphql_name='requestInput', default=None)),
))
    )
    request_invite = sgqlc.types.Field('SignupRequest', graphql_name='requestInvite', args=sgqlc.types.ArgDict((
        ('request_input', sgqlc.types.Arg(SignupRequestInput, graphql_name='requestInput', default=None)),
))
    )
    delete_invite = sgqlc.types.Field(DeleteInvite, graphql_name='deleteInvite', args=sgqlc.types.ArgDict((
        ('data', sgqlc.types.Arg(DeleteInviteInput, graphql_name='data', default=None)),
))
    )
    accept_invite = sgqlc.types.Field(AcceptInvite, graphql_name='acceptInvite', args=sgqlc.types.ArgDict((
        ('data', sgqlc.types.Arg(AcceptInviteInput, graphql_name='data', default=None)),
))
    )
    reject_invite = sgqlc.types.Field('RejectInvite', graphql_name='rejectInvite', args=sgqlc.types.ArgDict((
        ('data', sgqlc.types.Arg(RejectInviteInput, graphql_name='data', default=None)),
))
    )
    create_invite_link = sgqlc.types.Field(CreateInviteLink, graphql_name='createInviteLink', args=sgqlc.types.ArgDict((
        ('data', sgqlc.types.Arg(CreateInviteLinkInput, graphql_name='data', default=None)),
))
    )
    delete_invite_link = sgqlc.types.Field(DeleteInviteLink, graphql_name='deleteInviteLink', args=sgqlc.types.ArgDict((
        ('data', sgqlc.types.Arg(DeleteInviteLinkInput, graphql_name='data', default=None)),
))
    )
    forum = sgqlc.types.Field(ForumMutation, graphql_name='forum', args=sgqlc.types.ArgDict((
        ('forum_data', sgqlc.types.Arg(ForumInput, graphql_name='forumData', default=None)),
))
    )
    thread = sgqlc.types.Field('ThreadMutation', graphql_name='thread', args=sgqlc.types.ArgDict((
        ('thread_data', sgqlc.types.Arg(ThreadInput, graphql_name='threadData', default=None)),
))
    )
    category = sgqlc.types.Field(CategoryMutation, graphql_name='category', args=sgqlc.types.ArgDict((
        ('category_data', sgqlc.types.Arg(CategoryInput, graphql_name='categoryData', default=None)),
))
    )
    pin = sgqlc.types.Field('PinMutation', graphql_name='pin', args=sgqlc.types.ArgDict((
        ('pin_data', sgqlc.types.Arg(sgqlc.types.non_null(PinInput), graphql_name='pinData', default=None)),
))
    )
    billing_subscribe = sgqlc.types.Field(BillingSubscribeMutation, graphql_name='billingSubscribe', args=sgqlc.types.ArgDict((
        ('subscription_data', sgqlc.types.Arg(BillingSubscribeInput, graphql_name='subscriptionData', default=None)),
))
    )
    billing_cancel = sgqlc.types.Field(BillingCancelSubscriptionMutation, graphql_name='billingCancel', args=sgqlc.types.ArgDict((
        ('subscription_data', sgqlc.types.Arg(BillingCancelSubscriptionInput, graphql_name='subscriptionData', default=None)),
))
    )
    billing_add_seats = sgqlc.types.Field(BillingAddSeatsMutation, graphql_name='billingAddSeats', args=sgqlc.types.ArgDict((
        ('arguments', sgqlc.types.Arg(BillingAddSeatsInput, graphql_name='arguments', default=None)),
))
    )
    billing_remove_seats = sgqlc.types.Field(BillingRemoveSeatsMutation, graphql_name='billingRemoveSeats', args=sgqlc.types.ArgDict((
        ('arguments', sgqlc.types.Arg(BillingRemoveSeatsInput, graphql_name='arguments', default=None)),
))
    )
    add_payment_method = sgqlc.types.Field(AddPaymentMutation, graphql_name='addPaymentMethod', args=sgqlc.types.ArgDict((
        ('payment_method_data', sgqlc.types.Arg(AddPaymentMethodInput, graphql_name='paymentMethodData', default=None)),
))
    )
    delete_payment_method = sgqlc.types.Field(DeletePaymentMutation, graphql_name='deletePaymentMethod', args=sgqlc.types.ArgDict((
        ('payment_method_data', sgqlc.types.Arg(DeletePaymentMethodInput, graphql_name='paymentMethodData', default=None)),
))
    )
    make_default_payment_method = sgqlc.types.Field(MakeDefaultPaymentMethodMutation, graphql_name='makeDefaultPaymentMethod', args=sgqlc.types.ArgDict((
        ('payment_method_data', sgqlc.types.Arg(MakeDefaultPaymentMethodInput, graphql_name='paymentMethodData', default=None)),
))
    )
    mark_all_as_read = sgqlc.types.Field(MarkAllAsReadMutation, graphql_name='markAllAsRead')
    create_annotation = sgqlc.types.Field(sgqlc.types.non_null(Annotation), graphql_name='createAnnotation', args=sgqlc.types.ArgDict((
        ('create_annotation_input', sgqlc.types.Arg(CreateAnnotationInput, graphql_name='createAnnotationInput', default=None)),
))
    )
    delete_annotation = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='deleteAnnotation', args=sgqlc.types.ArgDict((
        ('delete_annotation_input', sgqlc.types.Arg(DeleteAnnotationInput, graphql_name='deleteAnnotationInput', default=None)),
))
    )
    create_assembly = sgqlc.types.Field(sgqlc.types.non_null('Assembly'), graphql_name='createAssembly', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssemblyInput), graphql_name='input', default=None)),
))
    )
    convert_assembly = sgqlc.types.Field(sgqlc.types.non_null('Assembly'), graphql_name='convertAssembly', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(ConvertAssemblyInput), graphql_name='input', default=None)),
))
    )
    create_address = sgqlc.types.Field(sgqlc.types.non_null('Address'), graphql_name='createAddress', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAddressInput), graphql_name='input', default=None)),
))
    )
    update_address = sgqlc.types.Field(sgqlc.types.non_null('Address'), graphql_name='updateAddress', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAddressInput), graphql_name='input', default=None)),
))
    )
    delete_address = sgqlc.types.Field(sgqlc.types.non_null('Address'), graphql_name='deleteAddress', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAddressInput), graphql_name='input', default=None)),
))
    )
    create_intermediator = sgqlc.types.Field(sgqlc.types.non_null('Intermediator'), graphql_name='createIntermediator', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateIntermediatorInput), graphql_name='input', default=None)),
))
    )
    create_manufacturer = sgqlc.types.Field(sgqlc.types.non_null('Manufacturer'), graphql_name='createManufacturer', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateManufacturerInput), graphql_name='input', default=None)),
))
    )
    update_manufacturer = sgqlc.types.Field(sgqlc.types.non_null('Manufacturer'), graphql_name='updateManufacturer', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateManufacturerInput), graphql_name='input', default=None)),
))
    )
    create_service_instances = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ServiceInstance'))), graphql_name='createServiceInstances', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateServiceInstancesInput), graphql_name='input', default=None)),
))
    )
    update_service_instance = sgqlc.types.Field(sgqlc.types.non_null('ServiceInstance'), graphql_name='updateServiceInstance', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateServiceInstanceInput), graphql_name='input', default=None)),
))
    )
    create_option_instances = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('OptionInstance'))), graphql_name='createOptionInstances', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateOptionInstancesInput), graphql_name='input', default=None)),
))
    )
    update_option_instance = sgqlc.types.Field(sgqlc.types.non_null('OptionInstance'), graphql_name='updateOptionInstance', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateOptionInstanceInput), graphql_name='input', default=None)),
))
    )
    create_materials = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Material'))), graphql_name='createMaterials', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateMaterialsInput), graphql_name='input', default=None)),
))
    )
    create_processes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Process'))), graphql_name='createProcesses', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateProcessesInput), graphql_name='input', default=None)),
))
    )
    create_min_max_option = sgqlc.types.Field(sgqlc.types.non_null('MinMaxOption'), graphql_name='createMinMaxOption', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateMinMaxOptionInput), graphql_name='input', default=None)),
))
    )
    create_selection_option = sgqlc.types.Field(sgqlc.types.non_null('SelectionOption'), graphql_name='createSelectionOption', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateSelectionOptionInput), graphql_name='input', default=None)),
))
    )
    create_message = sgqlc.types.Field(sgqlc.types.non_null('Message'), graphql_name='createMessage', args=sgqlc.types.ArgDict((
        ('create_message_input', sgqlc.types.Arg(CreateMessageInput, graphql_name='createMessageInput', default=None)),
))
    )
    update_message = sgqlc.types.Field(sgqlc.types.non_null('Message'), graphql_name='updateMessage', args=sgqlc.types.ArgDict((
        ('update_message_input', sgqlc.types.Arg(UpdateMessageInput, graphql_name='updateMessageInput', default=None)),
))
    )
    delete_message = sgqlc.types.Field(sgqlc.types.non_null('Message'), graphql_name='deleteMessage', args=sgqlc.types.ArgDict((
        ('delete_message_input', sgqlc.types.Arg(DeleteMessageInput, graphql_name='deleteMessageInput', default=None)),
))
    )
    create_order = sgqlc.types.Field(sgqlc.types.non_null('Order'), graphql_name='createOrder', args=sgqlc.types.ArgDict((
        ('create_order_input', sgqlc.types.Arg(sgqlc.types.non_null(CreateOrderInput), graphql_name='createOrderInput', default=None)),
))
    )
    update_order = sgqlc.types.Field(sgqlc.types.non_null('Order'), graphql_name='updateOrder', args=sgqlc.types.ArgDict((
        ('update_order_input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateOrderInput), graphql_name='updateOrderInput', default=None)),
))
    )
    confirm_order = sgqlc.types.Field(sgqlc.types.non_null('Order'), graphql_name='confirmOrder', args=sgqlc.types.ArgDict((
        ('confirm_order_input', sgqlc.types.Arg(sgqlc.types.non_null(ConfirmOrderInput), graphql_name='confirmOrderInput', default=None)),
))
    )
    cancel_order = sgqlc.types.Field(sgqlc.types.non_null('Order'), graphql_name='cancelOrder', args=sgqlc.types.ArgDict((
        ('cancel_order_input', sgqlc.types.Arg(sgqlc.types.non_null(CancelOrderInput), graphql_name='cancelOrderInput', default=None)),
))
    )
    create_request_for_quote = sgqlc.types.Field(sgqlc.types.non_null('RequestForQuote'), graphql_name='createRequestForQuote', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateRequestForQuotesInput), graphql_name='input', default=None)),
        ('space_id', sgqlc.types.Arg(ID, graphql_name='spaceId', default=None)),
))
    )
    close_request_for_quote = sgqlc.types.Field(sgqlc.types.non_null('RequestForQuote'), graphql_name='closeRequestForQuote', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CloseRequestForQuoteInput), graphql_name='input', default=None)),
))
    )
    update_request_for_quote = sgqlc.types.Field(sgqlc.types.non_null('RequestForQuote'), graphql_name='updateRequestForQuote', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateRequestForQuoteInput), graphql_name='input', default=None)),
))
    )
    assign_request_for_quote = sgqlc.types.Field(sgqlc.types.non_null('RequestForQuote'), graphql_name='assignRequestForQuote', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(AssignRequestForQuoteInput), graphql_name='input', default=None)),
))
    )
    close_session = sgqlc.types.Field(sgqlc.types.non_null('Session'), graphql_name='closeSession', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CloseSessionInput), graphql_name='input', default=None)),
))
    )
    create_quote = sgqlc.types.Field(sgqlc.types.non_null('Quote'), graphql_name='createQuote', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateQuoteInput), graphql_name='input', default=None)),
))
    )
    reject_quote = sgqlc.types.Field(sgqlc.types.non_null('Quote'), graphql_name='rejectQuote', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(RejectQuoteInput), graphql_name='input', default=None)),
))
    )


class NewPassword(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result', 'msg')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')
    msg = sgqlc.types.Field(String, graphql_name='msg')


class Node(sgqlc.types.Interface):
    __schema__ = WIF_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class Notification(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'type', 'when', 'author', 'target', 'read')
    id = sgqlc.types.Field(ID, graphql_name='id')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    when = sgqlc.types.Field(DateTime, graphql_name='when')
    author = sgqlc.types.Field('Profile', graphql_name='author')
    target = sgqlc.types.Field('NotificationTarget', graphql_name='target')
    read = sgqlc.types.Field(Boolean, graphql_name='read')


class NotificationCenter(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'pending_count', 'notifications')
    id = sgqlc.types.Field(ID, graphql_name='id')
    pending_count = sgqlc.types.Field(Int, graphql_name='pendingCount')
    notifications = sgqlc.types.Field('NotificationConnection', graphql_name='notifications', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class NotificationConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('NotificationEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class NotificationEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(Notification, graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class OperationMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'project')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    project = sgqlc.types.Field('Project', graphql_name='project')


class OpsConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('OpsEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class OpsEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('ContribOp', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class Option(sgqlc.types.Interface):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'name', 'for_', 'value_type', 'unit', 'required', 'nil_label', 'prefix', 'instances', 'values')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    for_ = sgqlc.types.Field(sgqlc.types.non_null('Optionable'), graphql_name='for')
    value_type = sgqlc.types.Field(sgqlc.types.non_null(OptionValueType), graphql_name='valueType')
    unit = sgqlc.types.Field(String, graphql_name='unit')
    required = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='required')
    nil_label = sgqlc.types.Field(String, graphql_name='nilLabel')
    prefix = sgqlc.types.Field(String, graphql_name='prefix')
    instances = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('OptionInstance')), graphql_name='instances', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(OptionFilter, graphql_name='filter', default=None)),
))
    )
    values = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('OptionValue')), graphql_name='values', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(OptionFilter, graphql_name='filter', default=None)),
))
    )


class OptionValue(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'option', 'default', 'value_int', 'value_float', 'value_string', 'value_bool')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    option = sgqlc.types.Field(sgqlc.types.non_null(Option), graphql_name='option')
    default = sgqlc.types.Field(Boolean, graphql_name='default')
    value_int = sgqlc.types.Field(Int, graphql_name='valueInt')
    value_float = sgqlc.types.Field(Float, graphql_name='valueFloat')
    value_string = sgqlc.types.Field(String, graphql_name='valueString')
    value_bool = sgqlc.types.Field(Boolean, graphql_name='valueBool')


class Optionable(sgqlc.types.Interface):
    __schema__ = WIF_schema
    __field_names__ = ('options',)
    options = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Option)), graphql_name='options')


class OrganizationType(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')


class Page(sgqlc.types.Interface):
    __schema__ = WIF_schema
    __field_names__ = ('nodes', 'total')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Node))), graphql_name='nodes')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class PageInfo(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('has_next_page', 'has_previous_page', 'start_cursor', 'end_cursor')
    has_next_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasNextPage')
    has_previous_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasPreviousPage')
    start_cursor = sgqlc.types.Field(String, graphql_name='startCursor')
    end_cursor = sgqlc.types.Field(String, graphql_name='endCursor')


class PinMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'thread')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    thread = sgqlc.types.Field('Thread', graphql_name='thread')


class PostConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('PostEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class PostEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Post', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PostMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'post')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    post = sgqlc.types.Field('Post', graphql_name='post')


class ProfileConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('ProfileEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class ProfileConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(ProfileConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class ProfileEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Profile', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ProfileIntent(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')


class ProfileUserType(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')


class ProjectConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('ProjectEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class ProjectConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(ProjectConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class ProjectEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Project', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ProjectMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'project')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    project = sgqlc.types.Field('Project', graphql_name='project')


class ProjectPhase(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'name', 'color', 'order')
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    color = sgqlc.types.Field(String, graphql_name='color')
    order = sgqlc.types.Field(Int, graphql_name='order')


class ProjectVisibilityMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class Query(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'user_by_id', 'user', 'slug', 'channel', 'channels', 'initiative', 'initiatives', 'organization_types', 'profile', 'profile_user_types', 'profile_intents', 'profiles', 'profiles_complete', 'channel_complete', 'skill_complete', 'can_create_in_spaces', 'licenses', 'post', 'posts', 'comments', 'story', 'stories', 'project', 'projects', 'suggested_projects', 'project_phases', 'shared_file', 'contribution_file', 'collection', 'collections', 'file', 'search', 'activity', 'global_activity', 'issues', 'viralresponse_issues', 'group', 'signup_invites', 'invite_link', 'groups', 'forum', 'forums', 'thread', 'threads', 'forum_category', 'logged_in_user', 'annotations', 'assemblies', 'invoice', 'invoices', 'address', 'addresses', 'manufacturer', 'manufacturers', 'materials', 'processes', 'services', 'options', 'option_instances', 'messages', 'order', 'orders', 'request_for_quote', 'request_for_quotes', 'session', 'sessions', 'quote', 'quotes')
    node = sgqlc.types.Field(Node, graphql_name='node', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    user_by_id = sgqlc.types.Field('User', graphql_name='userById', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )
    user = sgqlc.types.Field('User', graphql_name='user', args=sgqlc.types.ArgDict((
        ('username', sgqlc.types.Arg(String, graphql_name='username', default=None)),
))
    )
    slug = sgqlc.types.Field('SlugUnique', graphql_name='slug', args=sgqlc.types.ArgDict((
        ('slug_data', sgqlc.types.Arg(SlugInput, graphql_name='slugData', default=None)),
))
    )
    channel = sgqlc.types.Field('channelErrorHandler', graphql_name='channel', args=sgqlc.types.ArgDict((
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
))
    )
    channels = sgqlc.types.Field(ChannelConnectionErrorHandler, graphql_name='channels', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    initiative = sgqlc.types.Field('initiativeErrorHandler', graphql_name='initiative', args=sgqlc.types.ArgDict((
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )
    initiatives = sgqlc.types.Field(InitiativeConnectionErrorHandler, graphql_name='initiatives', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    organization_types = sgqlc.types.Field(sgqlc.types.list_of(OrganizationType), graphql_name='organizationTypes')
    profile = sgqlc.types.Field('profileErrorHandler', graphql_name='profile', args=sgqlc.types.ArgDict((
        ('username', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='username', default=None)),
))
    )
    profile_user_types = sgqlc.types.Field(sgqlc.types.list_of(ProfileUserType), graphql_name='profileUserTypes')
    profile_intents = sgqlc.types.Field(sgqlc.types.list_of(ProfileIntent), graphql_name='profileIntents')
    profiles = sgqlc.types.Field(ProfileConnectionErrorHandler, graphql_name='profiles', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    profiles_complete = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='profilesComplete', args=sgqlc.types.ArgDict((
        ('complete', sgqlc.types.Arg(String, graphql_name='complete', default=None)),
))
    )
    channel_complete = sgqlc.types.Field(sgqlc.types.list_of('Channel'), graphql_name='channelComplete', args=sgqlc.types.ArgDict((
        ('complete', sgqlc.types.Arg(String, graphql_name='complete', default=None)),
))
    )
    skill_complete = sgqlc.types.Field(sgqlc.types.list_of('Skill'), graphql_name='skillComplete', args=sgqlc.types.ArgDict((
        ('complete', sgqlc.types.Arg(String, graphql_name='complete', default=None)),
))
    )
    can_create_in_spaces = sgqlc.types.Field(sgqlc.types.list_of('Space'), graphql_name='canCreateInSpaces', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(String, graphql_name='type', default=None)),
        ('obj', sgqlc.types.Arg(JSONString, graphql_name='obj', default=None)),
))
    )
    licenses = sgqlc.types.Field(sgqlc.types.list_of(License), graphql_name='licenses')
    post = sgqlc.types.Field('postErrorHandler', graphql_name='post', args=sgqlc.types.ArgDict((
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
))
    )
    posts = sgqlc.types.Field(PostConnection, graphql_name='posts', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    story = sgqlc.types.Field('storyErrorHandler', graphql_name='story', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(String, graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )
    stories = sgqlc.types.Field('StoryConnectionErrorHandler', graphql_name='stories', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    project = sgqlc.types.Field('projectErrorHandler', graphql_name='project', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(String, graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )
    projects = sgqlc.types.Field(ProjectConnectionErrorHandler, graphql_name='projects', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    suggested_projects = sgqlc.types.Field('SuggestedProjectConnectionErrorHandler', graphql_name='suggestedProjects', args=sgqlc.types.ArgDict((
        ('project_id', sgqlc.types.Arg(ID, graphql_name='projectId', default=None)),
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    project_phases = sgqlc.types.Field(sgqlc.types.list_of(ProjectPhase), graphql_name='projectPhases')
    shared_file = sgqlc.types.Field('shared_fileErrorHandler', graphql_name='sharedFile', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('version', sgqlc.types.Arg(String, graphql_name='version', default=None)),
))
    )
    contribution_file = sgqlc.types.Field('contribution_fileErrorHandler', graphql_name='contributionFile', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='slug', default=None)),
        ('dirname', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='dirname', default=None)),
        ('filename', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='filename', default=None)),
        ('version', sgqlc.types.Arg(String, graphql_name='version', default=None)),
))
    )
    collection = sgqlc.types.Field('collectionErrorHandler', graphql_name='collection', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(String, graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )
    collections = sgqlc.types.Field(CollectionConnectionErrorHandler, graphql_name='collections', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    file = sgqlc.types.Field('fileErrorHandler', graphql_name='file', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(String, graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )
    search = sgqlc.types.Field('SearchResult', graphql_name='search', args=sgqlc.types.ArgDict((
        ('q', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='q', default=None)),
))
    )
    activity = sgqlc.types.Field(ActivityConnection, graphql_name='activity', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    global_activity = sgqlc.types.Field(ActivityConnection, graphql_name='globalActivity', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    issues = sgqlc.types.Field(IssueConnectionErrorHandler, graphql_name='issues', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    viralresponse_issues = sgqlc.types.Field('ViralResponseIssueConnectionErrorHandler', graphql_name='viralresponseIssues', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    group = sgqlc.types.Field('groupErrorHandler', graphql_name='group', args=sgqlc.types.ArgDict((
        ('space_id', sgqlc.types.Arg(ID, graphql_name='spaceId', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
))
    )
    signup_invites = sgqlc.types.Field(sgqlc.types.list_of('GroupInvite'), graphql_name='signupInvites')
    invite_link = sgqlc.types.Field('invite_linkErrorHandler', graphql_name='inviteLink', args=sgqlc.types.ArgDict((
        ('token', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='token', default=None)),
        ('invite_link_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='inviteLinkId', default=None)),
        ('referrer_user_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='referrerUserId', default=None)),
))
    )
    groups = sgqlc.types.Field(sgqlc.types.list_of('Group'), graphql_name='groups', args=sgqlc.types.ArgDict((
        ('space_slug', sgqlc.types.Arg(String, graphql_name='spaceSlug', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
))
    )
    forum = sgqlc.types.Field('forumErrorHandler', graphql_name='forum', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='space', default=None)),
))
    )
    forums = sgqlc.types.Field(ForumConnectionErrorHandler, graphql_name='forums', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    thread = sgqlc.types.Field('threadErrorHandler', graphql_name='thread', args=sgqlc.types.ArgDict((
        ('url_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='urlId', default=None)),
))
    )
    threads = sgqlc.types.Field('ThreadConnectionErrorHandler', graphql_name='threads', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    forum_category = sgqlc.types.Field('forum_categoryErrorHandler', graphql_name='forumCategory', args=sgqlc.types.ArgDict((
        ('url_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='urlId', default=None)),
))
    )
    logged_in_user = sgqlc.types.Field('LoggedInUser', graphql_name='loggedInUser')
    annotations = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Annotation))), graphql_name='annotations', args=sgqlc.types.ArgDict((
        ('get_annotations_input', sgqlc.types.Arg(GetAnnotationsInput, graphql_name='getAnnotationsInput', default=None)),
))
    )
    assemblies = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Assembly'))), graphql_name='assemblies', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(GetAssembliesInput), graphql_name='input', default=None)),
))
    )
    invoice = sgqlc.types.Field(sgqlc.types.non_null('Invoice'), graphql_name='invoice', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    invoices = sgqlc.types.Field(sgqlc.types.non_null('InvoicePage'), graphql_name='invoices', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    address = sgqlc.types.Field(sgqlc.types.non_null('Address'), graphql_name='address', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    addresses = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Address'))), graphql_name='addresses', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(GetAddressesInput), graphql_name='input', default=None)),
))
    )
    manufacturer = sgqlc.types.Field('Manufacturer', graphql_name='manufacturer', args=sgqlc.types.ArgDict((
        ('manufacturer_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='manufacturerId', default=None)),
))
    )
    manufacturers = sgqlc.types.Field(sgqlc.types.non_null('ManufacturerPage'), graphql_name='manufacturers', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('filter', sgqlc.types.Arg(ManufacturerFilter, graphql_name='filter', default=None)),
))
    )
    materials = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Material'))), graphql_name='materials', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(MaterialFilter, graphql_name='filter', default=None)),
))
    )
    processes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Process'))), graphql_name='processes', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ProcessFilter, graphql_name='filter', default=None)),
))
    )
    services = sgqlc.types.Field(sgqlc.types.non_null('ServicePage'), graphql_name='services', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('filter', sgqlc.types.Arg(ServiceFilter, graphql_name='filter', default=None)),
))
    )
    options = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Option))), graphql_name='options', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(OptionFilter, graphql_name='filter', default=None)),
))
    )
    option_instances = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('OptionInstance'))), graphql_name='optionInstances', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(OptionInstanceFilter, graphql_name='filter', default=None)),
))
    )
    messages = sgqlc.types.Field(sgqlc.types.non_null('MessagePage'), graphql_name='messages', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('get_messages_input', sgqlc.types.Arg(GetMessagesInput, graphql_name='getMessagesInput', default=None)),
))
    )
    order = sgqlc.types.Field(sgqlc.types.non_null('Order'), graphql_name='order', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    orders = sgqlc.types.Field(sgqlc.types.non_null('OrderPage'), graphql_name='orders', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    request_for_quote = sgqlc.types.Field('RequestForQuote', graphql_name='requestForQuote', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    request_for_quotes = sgqlc.types.Field(sgqlc.types.non_null('RequestForQuotePage'), graphql_name='requestForQuotes', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sort_field', sgqlc.types.Arg(String, graphql_name='sortField', default=None)),
        ('sort_order', sgqlc.types.Arg(SortOrder, graphql_name='sortOrder', default=None)),
        ('filters', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(FilterInput)), graphql_name='filters', default=None)),
))
    )
    session = sgqlc.types.Field('Session', graphql_name='session', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    sessions = sgqlc.types.Field(sgqlc.types.non_null('SessionPage'), graphql_name='sessions', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('filter_input', sgqlc.types.Arg(SessionFilterInput, graphql_name='filterInput', default=None)),
))
    )
    quote = sgqlc.types.Field('Quote', graphql_name='quote', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    quotes = sgqlc.types.Field(sgqlc.types.non_null('QuotePage'), graphql_name='quotes', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sort_field', sgqlc.types.Arg(String, graphql_name='sortField', default=None)),
        ('sort_order', sgqlc.types.Arg(SortOrder, graphql_name='sortOrder', default=None)),
        ('filters', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(FilterInput)), graphql_name='filters', default=None)),
))
    )


class RejectInvite(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class RemoveUserFromGroup(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'group', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    group = sgqlc.types.Field('Group', graphql_name='group')
    result = sgqlc.types.Field(String, graphql_name='result')


class RequestResetPassword(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class ResendInvite(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class ResetContributionMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'project')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    project = sgqlc.types.Field('Project', graphql_name='project')


class SearchResult(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('profiles', 'projects', 'initiatives', 'stories', 'collections', 'threads', 'channels')
    profiles = sgqlc.types.Field(ProfileConnection, graphql_name='profiles', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    projects = sgqlc.types.Field(ProjectConnection, graphql_name='projects', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    initiatives = sgqlc.types.Field(InitiativeConnection, graphql_name='initiatives', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    stories = sgqlc.types.Field('StoryConnection', graphql_name='stories', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    collections = sgqlc.types.Field(CollectionConnection, graphql_name='collections', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    threads = sgqlc.types.Field('ThreadConnection', graphql_name='threads', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    channels = sgqlc.types.Field(ChannelConnection, graphql_name='channels', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class SeatsUsage(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'used_space_seats', 'used_projects_seats', 'used_invites_seats', 'unused_seats', 'included_plan_seats', 'purchased_seats', 'total_sub_seats', 'seats_change')
    id = sgqlc.types.Field(ID, graphql_name='id')
    used_space_seats = sgqlc.types.Field(Int, graphql_name='usedSpaceSeats')
    used_projects_seats = sgqlc.types.Field(Int, graphql_name='usedProjectsSeats')
    used_invites_seats = sgqlc.types.Field(Int, graphql_name='usedInvitesSeats')
    unused_seats = sgqlc.types.Field(Int, graphql_name='unusedSeats')
    included_plan_seats = sgqlc.types.Field(Int, graphql_name='includedPlanSeats')
    purchased_seats = sgqlc.types.Field(Int, graphql_name='purchasedSeats')
    total_sub_seats = sgqlc.types.Field(Int, graphql_name='totalSubSeats')
    seats_change = sgqlc.types.Field(Int, graphql_name='seatsChange')


class SharedFileConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('SharedFileEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class SharedFileEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('SharedFile', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class SharedFileRevision(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'version', 'date_created', 'last_updated', 'title', 'creator', 'file')
    id = sgqlc.types.Field(ID, graphql_name='id')
    version = sgqlc.types.Field(String, graphql_name='version')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    title = sgqlc.types.Field(String, graphql_name='title')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    file = sgqlc.types.Field('File', graphql_name='file')


class SharedFileRevisionConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('SharedFileRevisionEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class SharedFileRevisionEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(SharedFileRevision, graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class SignupRequest(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class SlugUnique(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('value', 'unique')
    value = sgqlc.types.Field(String, graphql_name='value')
    unique = sgqlc.types.Field(Boolean, graphql_name='unique')


class StoryConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('StoryEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class StoryConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(StoryConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class StoryEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Story', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class StoryMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'story')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    story = sgqlc.types.Field('Story', graphql_name='story')


class SubscriptionPreview(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'total_amount', 'per_seat_amount', 'initial_amount', 'billing_starts', 'proration_amount', 'proration_timestamp', 'discount_amount', 'seats')
    id = sgqlc.types.Field(ID, graphql_name='id')
    total_amount = sgqlc.types.Field(Int, graphql_name='totalAmount')
    per_seat_amount = sgqlc.types.Field(Int, graphql_name='perSeatAmount')
    initial_amount = sgqlc.types.Field(Int, graphql_name='initialAmount')
    billing_starts = sgqlc.types.Field(DateTime, graphql_name='billingStarts')
    proration_amount = sgqlc.types.Field(Int, graphql_name='prorationAmount')
    proration_timestamp = sgqlc.types.Field(Int, graphql_name='prorationTimestamp')
    discount_amount = sgqlc.types.Field(Int, graphql_name='discountAmount')
    seats = sgqlc.types.Field(SeatsUsage, graphql_name='seats')


class SuggestedProjectConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('SuggestedProjectEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class SuggestedProjectConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(SuggestedProjectConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('project_id', sgqlc.types.Arg(ID, graphql_name='projectId', default=None)),
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class SuggestedProjectEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Project', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class Supplier(sgqlc.types.Interface):
    __schema__ = WIF_schema
    __field_names__ = ('id', 'initiative', 'space', 'address')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    initiative = sgqlc.types.Field(sgqlc.types.non_null('FederatedInitiative'), graphql_name='initiative')
    space = sgqlc.types.Field(sgqlc.types.non_null('Space'), graphql_name='space')
    address = sgqlc.types.Field(sgqlc.types.non_null('Address'), graphql_name='address')


class Target(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('target_type', 'sel_type', 'instance_ix', 'brep_ix', 'body_ix', 'prc_path', 'face_hit', 'face_ix', 'loop_ix', 'edge_ix', 'point_hit', 'point_ix', 'triangle_ix', 'triangle_pt', 'triangle_nr')
    target_type = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='targetType')
    sel_type = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='selType')
    instance_ix = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='instanceIx')
    brep_ix = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='brepIx')
    body_ix = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='bodyIx')
    prc_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='prcPath')
    face_hit = sgqlc.types.Field(Boolean, graphql_name='faceHit')
    face_ix = sgqlc.types.Field(Int, graphql_name='faceIx')
    loop_ix = sgqlc.types.Field(Int, graphql_name='loopIx')
    edge_ix = sgqlc.types.Field(Int, graphql_name='edgeIx')
    point_hit = sgqlc.types.Field(Boolean, graphql_name='pointHit')
    point_ix = sgqlc.types.Field(Int, graphql_name='pointIx')
    triangle_ix = sgqlc.types.Field(Int, graphql_name='triangleIx')
    triangle_pt = sgqlc.types.Field('Vector', graphql_name='trianglePt')
    triangle_nr = sgqlc.types.Field('Vector', graphql_name='triangleNr')


class ThreadConnection(sgqlc.types.relay.Connection):
    __schema__ = WIF_schema
    __field_names__ = ('page_info', 'edges', 'total_count')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('ThreadEdge')), graphql_name='edges')
    total_count = sgqlc.types.Field(Int, graphql_name='totalCount')


class ThreadConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(ThreadConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class ThreadEdge(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('Thread', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ThreadMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'thread')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    thread = sgqlc.types.Field('Thread', graphql_name='thread')


class TransferProjectMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'project')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    project = sgqlc.types.Field('Project', graphql_name='project')


class UpdateImportProjectMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    result = sgqlc.types.Field(String, graphql_name='result')


class UpdateProfile(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'profile')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    profile = sgqlc.types.Field('Profile', graphql_name='profile')


class UpdateSharedFileMutation(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'shared_file')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of('UserError'), graphql_name='userErrors')
    shared_file = sgqlc.types.Field('SharedFile', graphql_name='sharedFile')


class UserError(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('code', 'message', 'key')
    code = sgqlc.types.Field(ErrorCodes, graphql_name='code')
    message = sgqlc.types.Field(String, graphql_name='message')
    key = sgqlc.types.Field(String, graphql_name='key')


class Vector(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('x', 'y', 'z')
    x = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='x')
    y = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='y')
    z = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='z')


class ViralResponseIssueConnectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field(IssueConnection, graphql_name='result', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class channelErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Channel', graphql_name='result', args=sgqlc.types.ArgDict((
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
))
    )


class collectionErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Collection', graphql_name='result', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(String, graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )


class contribution_fileErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('ContribFile', graphql_name='result', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='slug', default=None)),
        ('dirname', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='dirname', default=None)),
        ('filename', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='filename', default=None)),
        ('version', sgqlc.types.Arg(String, graphql_name='version', default=None)),
))
    )


class fileErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('File', graphql_name='result', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(String, graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )


class forumErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Forum', graphql_name='result', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='space', default=None)),
))
    )


class forum_categoryErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Category', graphql_name='result', args=sgqlc.types.ArgDict((
        ('url_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='urlId', default=None)),
))
    )


class groupErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Group', graphql_name='result', args=sgqlc.types.ArgDict((
        ('space_id', sgqlc.types.Arg(ID, graphql_name='spaceId', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
))
    )


class initiativeErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Initiative', graphql_name='result', args=sgqlc.types.ArgDict((
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )


class invite_linkErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('InviteLink', graphql_name='result', args=sgqlc.types.ArgDict((
        ('token', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='token', default=None)),
        ('invite_link_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='inviteLinkId', default=None)),
        ('referrer_user_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='referrerUserId', default=None)),
))
    )


class postErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Post', graphql_name='result', args=sgqlc.types.ArgDict((
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
))
    )


class profileErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Profile', graphql_name='result', args=sgqlc.types.ArgDict((
        ('username', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='username', default=None)),
))
    )


class projectErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Project', graphql_name='result', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(String, graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )


class shared_fileErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('SharedFile', graphql_name='result', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('version', sgqlc.types.Arg(String, graphql_name='version', default=None)),
))
    )


class storyErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Story', graphql_name='result', args=sgqlc.types.ArgDict((
        ('space', sgqlc.types.Arg(String, graphql_name='space', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
))
    )


class threadErrorHandler(sgqlc.types.Type):
    __schema__ = WIF_schema
    __field_names__ = ('user_errors', 'result')
    user_errors = sgqlc.types.Field(sgqlc.types.list_of(UserError), graphql_name='userErrors')
    result = sgqlc.types.Field('Thread', graphql_name='result', args=sgqlc.types.ArgDict((
        ('url_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='urlId', default=None)),
))
    )


class ActivityContent(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'slug', 'creator_id', 'created_in_region', 'space_id', 'date_created', 'last_updated', 'whitelabel', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'comments_count', 'likes_count', 'followers_count', 'score', 'pageviews_count', 'public_read', 'registered_read', 'featured_in', 'creator', 'followers', 'tags', 'comments', 'can_update', 'can_delete', 'parent_slug', 'is_private', 'description', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'title', 'commenters', 'page_views', 'version', 'origin')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    whitelabel = sgqlc.types.Field(String, graphql_name='whitelabel')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    comments_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentsCount')
    likes_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likesCount')
    followers_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='followersCount')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    parent_slug = sgqlc.types.Field(String, graphql_name='parentSlug')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    description = sgqlc.types.Field(String, graphql_name='description')
    content = sgqlc.types.Field('Content', graphql_name='content')
    parent_content = sgqlc.types.Field('Content', graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    version = sgqlc.types.Field(String, graphql_name='version')
    origin = sgqlc.types.Field('Content', graphql_name='origin')


class ActivityOrigin(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'slug', 'creator_id', 'created_in_region', 'space_id', 'date_created', 'last_updated', 'whitelabel', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'comments_count', 'likes_count', 'followers_count', 'score', 'pageviews_count', 'public_read', 'registered_read', 'featured_in', 'creator', 'followers', 'tags', 'comments', 'can_update', 'can_delete', 'parent_slug', 'is_private', 'description', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'title', 'commenters', 'page_views')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    whitelabel = sgqlc.types.Field(String, graphql_name='whitelabel')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    comments_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentsCount')
    likes_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likesCount')
    followers_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='followersCount')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    parent_slug = sgqlc.types.Field(String, graphql_name='parentSlug')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    description = sgqlc.types.Field(String, graphql_name='description')
    content = sgqlc.types.Field('Content', graphql_name='content')
    parent_content = sgqlc.types.Field('Content', graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')


class Address(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'address1', 'address2', 'city', 'province', 'country', 'zip', 'phone', 'company', 'default')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    address1 = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='address1')
    address2 = sgqlc.types.Field(String, graphql_name='address2')
    city = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='city')
    province = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='province')
    country = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='country')
    zip = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='zip')
    phone = sgqlc.types.Field(String, graphql_name='phone')
    company = sgqlc.types.Field(String, graphql_name='company')
    default = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='default')


class Assembly(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('file_id', 'parts', 'cad_conversions')
    file_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='fileId')
    parts = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Part'))), graphql_name='parts')
    cad_conversions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('CadConversion'))), graphql_name='cadConversions')


class BillingInvoice(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('subscription_id', 'status', 'period_start', 'period_end', 'number', 'amount', 'download_url', 'payment_method', 'subscription')
    subscription_id = sgqlc.types.Field(Int, graphql_name='subscriptionId')
    status = sgqlc.types.Field(String, graphql_name='status')
    period_start = sgqlc.types.Field(DateTime, graphql_name='periodStart')
    period_end = sgqlc.types.Field(DateTime, graphql_name='periodEnd')
    number = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='number')
    amount = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='amount')
    download_url = sgqlc.types.Field(String, graphql_name='downloadUrl')
    payment_method = sgqlc.types.Field(String, graphql_name='paymentMethod')
    subscription = sgqlc.types.Field('BillingSubscription', graphql_name='subscription')


class BillingPlan(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('product_id', 'name', 'type', 'currency', 'per_seat_amount', 'initial_amount')
    product_id = sgqlc.types.Field(Int, graphql_name='productId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    type = sgqlc.types.Field(sgqlc.types.non_null(plantype), graphql_name='type')
    currency = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='currency')
    per_seat_amount = sgqlc.types.Field(Int, graphql_name='perSeatAmount')
    initial_amount = sgqlc.types.Field(Int, graphql_name='initialAmount')


class BillingSubscription(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('plan_id', 'space_id', 'status', 'cancel_at_period_end', 'current_period_start', 'current_period_end', 'next_amount', 'trial_end', 'purchased_seats', 'seats_included', 'plan', 'invoices', 'last_invoice', 'seats', 'add_seats_preview', 'remove_seats_preview', 'sca_secret')
    plan_id = sgqlc.types.Field(Int, graphql_name='planId')
    space_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='spaceId')
    status = sgqlc.types.Field(sgqlc.types.non_null(subscriptionstatus), graphql_name='status')
    cancel_at_period_end = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='cancelAtPeriodEnd')
    current_period_start = sgqlc.types.Field(DateTime, graphql_name='currentPeriodStart')
    current_period_end = sgqlc.types.Field(DateTime, graphql_name='currentPeriodEnd')
    next_amount = sgqlc.types.Field(Int, graphql_name='nextAmount')
    trial_end = sgqlc.types.Field(DateTime, graphql_name='trialEnd')
    purchased_seats = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='purchasedSeats')
    seats_included = sgqlc.types.Field(Int, graphql_name='SeatsIncluded')
    plan = sgqlc.types.Field(BillingPlan, graphql_name='plan')
    invoices = sgqlc.types.Field(AutoBillingInvoiceConnection, graphql_name='invoices', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    last_invoice = sgqlc.types.Field(BillingInvoice, graphql_name='lastInvoice')
    seats = sgqlc.types.Field(SeatsUsage, graphql_name='seats')
    add_seats_preview = sgqlc.types.Field(SubscriptionPreview, graphql_name='addSeatsPreview', args=sgqlc.types.ArgDict((
        ('n_seats', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='nSeats', default=None)),
))
    )
    remove_seats_preview = sgqlc.types.Field(SubscriptionPreview, graphql_name='removeSeatsPreview', args=sgqlc.types.ArgDict((
        ('n_seats', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='nSeats', default=None)),
))
    )
    sca_secret = sgqlc.types.Field(String, graphql_name='scaSecret')


class Build(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('file', 'material', 'process', 'values')
    file = sgqlc.types.Field(sgqlc.types.non_null('FederatedFile'), graphql_name='file')
    material = sgqlc.types.Field(sgqlc.types.non_null('Material'), graphql_name='material')
    process = sgqlc.types.Field(sgqlc.types.non_null('Process'), graphql_name='process')
    values = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(BuildValue)), graphql_name='values')


class CadConversion(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('status', 'error', 'format', 'url', 'cad_id')
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='status')
    error = sgqlc.types.Field(String, graphql_name='error')
    format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='format')
    url = sgqlc.types.Field(String, graphql_name='url')
    cad_id = sgqlc.types.Field(String, graphql_name='cadId')


class Category(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('title', 'description', 'color', 'forum_id', 'threads_count', 'threads_count_public', 'forum', 'pinned', 'threads', 'url_id', 'can_update', 'can_delete', 'private_threads_count', 'last_active_thread')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    color = sgqlc.types.Field(String, graphql_name='color')
    forum_id = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='forumId')
    threads_count = sgqlc.types.Field(Int, graphql_name='threadsCount')
    threads_count_public = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='threadsCountPublic')
    forum = sgqlc.types.Field('Forum', graphql_name='forum')
    pinned = sgqlc.types.Field(sgqlc.types.list_of('Thread'), graphql_name='pinned')
    threads = sgqlc.types.Field(ThreadConnection, graphql_name='threads', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    url_id = sgqlc.types.Field(String, graphql_name='urlId')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    private_threads_count = sgqlc.types.Field(Int, graphql_name='privateThreadsCount')
    last_active_thread = sgqlc.types.Field('Thread', graphql_name='lastActiveThread')


class Certificate(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'file')
    name = sgqlc.types.Field(sgqlc.types.non_null(Certification), graphql_name='name')
    file = sgqlc.types.Field('FederatedFile', graphql_name='file')


class Channel(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'slug', 'created_in_region', 'date_created', 'last_updated', 'whitelabel', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'comments_count', 'likes_count', 'followers_count', 'score', 'pageviews_count', 'public_read', 'registered_read', 'name', 'description', 'ctas', 'configuration', 'tagged_count', 'featured_in', 'avatar', 'story', 'creator', 'followers', 'tags', 'comments', 'social_accounts', 'forum', 'following_count', 'can_update', 'can_delete', 'parent_slug', 'is_private', 'content', 'parent_content', 'in_space', 'image_fallback_char', 'title', 'commenters', 'page_views', 'moderators', 'posts', 'projects', 'stories', 'threads', 'collections', 'has_moderators')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    whitelabel = sgqlc.types.Field(String, graphql_name='whitelabel')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    comments_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentsCount')
    likes_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likesCount')
    followers_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='followersCount')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    ctas = sgqlc.types.Field(JSONString, graphql_name='ctas')
    configuration = sgqlc.types.Field(JSONString, graphql_name='configuration')
    tagged_count = sgqlc.types.Field(Int, graphql_name='taggedCount')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    story = sgqlc.types.Field('Story', graphql_name='story')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    social_accounts = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socialAccounts')
    forum = sgqlc.types.Field('Forum', graphql_name='forum')
    following_count = sgqlc.types.Field(Int, graphql_name='followingCount')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    parent_slug = sgqlc.types.Field(String, graphql_name='parentSlug')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    content = sgqlc.types.Field('Content', graphql_name='content')
    parent_content = sgqlc.types.Field('Content', graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    moderators = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='moderators')
    posts = sgqlc.types.Field(PostConnection, graphql_name='posts', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    projects = sgqlc.types.Field(ProjectConnection, graphql_name='projects', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    stories = sgqlc.types.Field(StoryConnection, graphql_name='stories', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    threads = sgqlc.types.Field(ThreadConnection, graphql_name='threads', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    collections = sgqlc.types.Field(CollectionConnection, graphql_name='collections', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    has_moderators = sgqlc.types.Field(Boolean, graphql_name='hasModerators')


class Collection(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'slug', 'creator_id', 'created_in_region', 'space_id', 'date_created', 'last_updated', 'whitelabel', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'comments_count', 'likes_count', 'followers_count', 'score', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'name', 'description', 'projects_count', 'featured_in', 'creator', 'space', 'followers', 'tags', 'projects', 'comments', 'can_update', 'can_delete', 'parent_slug', 'is_private', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'title', 'commenters', 'page_views', 'images', 'creator_profile')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    whitelabel = sgqlc.types.Field(String, graphql_name='whitelabel')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    comments_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentsCount')
    likes_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likesCount')
    followers_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='followersCount')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    projects_count = sgqlc.types.Field(Int, graphql_name='projectsCount')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    space = sgqlc.types.Field('Space', graphql_name='space')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    projects = sgqlc.types.Field(ProjectConnection, graphql_name='projects', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    parent_slug = sgqlc.types.Field(String, graphql_name='parentSlug')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    content = sgqlc.types.Field('Content', graphql_name='content')
    parent_content = sgqlc.types.Field('Content', graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    images = sgqlc.types.Field(sgqlc.types.list_of('File'), graphql_name='images')
    creator_profile = sgqlc.types.Field('Profile', graphql_name='creatorProfile')


class Comment(sgqlc.types.Type, Node, ContentInterface):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'creator_id', 'created_in_region', 'space_id', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'score', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'body', 'origin_id', 'replyto_id', 'featured_in', 'origin', 'replyto', 'followers', 'tags', 'comments', 'can_update', 'can_delete', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'title', 'commenters', 'page_views', 'creator_profile')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='body')
    origin_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='originId')
    replyto_id = sgqlc.types.Field(Int, graphql_name='replytoId')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    origin = sgqlc.types.Field(ContentInterface, graphql_name='origin')
    replyto = sgqlc.types.Field('Comment', graphql_name='replyto')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field('Content', graphql_name='content')
    parent_content = sgqlc.types.Field('Content', graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    creator_profile = sgqlc.types.Field('Profile', graphql_name='creatorProfile')


class Content(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('can_update', 'can_delete', 'type', 'slug', 'parent_slug', 'is_private', 'description', 'creator', 'date_created', 'last_updated', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'title', 'tags', 'comments', 'commenters', 'page_views', 'followers', 'likes_count', 'followers_count', 'comments_count', 'is_liked', 'version', 'whitelabel', 'is_followed')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    type = sgqlc.types.Field(String, graphql_name='type')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    parent_slug = sgqlc.types.Field(String, graphql_name='parentSlug')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    description = sgqlc.types.Field(String, graphql_name='description')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    content = sgqlc.types.Field('Content', graphql_name='content')
    parent_content = sgqlc.types.Field('Content', graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    likes_count = sgqlc.types.Field(Int, graphql_name='likesCount')
    followers_count = sgqlc.types.Field(Int, graphql_name='followersCount')
    comments_count = sgqlc.types.Field(Int, graphql_name='commentsCount')
    is_liked = sgqlc.types.Field(Boolean, graphql_name='isLiked')
    version = sgqlc.types.Field(String, graphql_name='version')
    whitelabel = sgqlc.types.Field(String, graphql_name='whitelabel')
    is_followed = sgqlc.types.Field(Boolean, graphql_name='isFollowed')


class Context(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('parent', 'parent_obj')
    parent = sgqlc.types.Field('Project', graphql_name='parent')
    parent_obj = sgqlc.types.Field('Project', graphql_name='parentObj')


class ContribFile(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('file', 'dirname', 'filename', 'is_folder', 'contribution', 'origin', 'last_updated')
    file = sgqlc.types.Field('File', graphql_name='file')
    dirname = sgqlc.types.Field(String, graphql_name='dirname')
    filename = sgqlc.types.Field(String, graphql_name='filename')
    is_folder = sgqlc.types.Field(Boolean, graphql_name='isFolder')
    contribution = sgqlc.types.Field('Contribution', graphql_name='contribution')
    origin = sgqlc.types.Field('Contribution', graphql_name='origin')
    last_updated = sgqlc.types.Field(String, graphql_name='lastUpdated')


class ContribOp(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('file', 'old_file', 'path', 'old_path', 'op_type', 'origin')
    file = sgqlc.types.Field('File', graphql_name='file')
    old_file = sgqlc.types.Field('File', graphql_name='oldFile')
    path = sgqlc.types.Field(String, graphql_name='path')
    old_path = sgqlc.types.Field(String, graphql_name='oldPath')
    op_type = sgqlc.types.Field(String, graphql_name='opType')
    origin = sgqlc.types.Field('Contribution', graphql_name='origin')


class Contribution(sgqlc.types.Type, Node, ContentInterface):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'creator_id', 'created_in_region', 'space_id', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'score', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'project_id', 'parent_id', 'status', 'title', 'version', 'old_version', 'zip_archive_generated_id', 'featured_in', 'project', 'children', 'parent', 'zip_archive_generated', 'followers', 'tags', 'comments', 'can_update', 'can_delete', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'commenters', 'page_views', 'operations', 'zip_archive_url', 'creator_profile', 'files_count', 'files', 'contrib_file')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='projectId')
    parent_id = sgqlc.types.Field(Int, graphql_name='parentId')
    status = sgqlc.types.Field(String, graphql_name='status')
    title = sgqlc.types.Field(String, graphql_name='title')
    version = sgqlc.types.Field(String, graphql_name='version')
    old_version = sgqlc.types.Field(Int, graphql_name='oldVersion')
    zip_archive_generated_id = sgqlc.types.Field(Int, graphql_name='zipArchiveGeneratedId')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    project = sgqlc.types.Field('Project', graphql_name='project')
    children = sgqlc.types.Field(sgqlc.types.list_of('Contribution'), graphql_name='children')
    parent = sgqlc.types.Field('Contribution', graphql_name='parent')
    zip_archive_generated = sgqlc.types.Field(Boolean, graphql_name='zipArchiveGenerated')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    operations = sgqlc.types.Field(sgqlc.types.list_of(ContribOp), graphql_name='operations')
    zip_archive_url = sgqlc.types.Field(String, graphql_name='zipArchiveUrl')
    creator_profile = sgqlc.types.Field('Profile', graphql_name='creatorProfile')
    files_count = sgqlc.types.Field(Int, graphql_name='filesCount')
    files = sgqlc.types.Field(sgqlc.types.list_of(ContribFile), graphql_name='files', args=sgqlc.types.ArgDict((
        ('basepath', sgqlc.types.Arg(String, graphql_name='basepath', default=None)),
))
    )
    contrib_file = sgqlc.types.Field(ContribFile, graphql_name='contribFile', args=sgqlc.types.ArgDict((
        ('filepath', sgqlc.types.Arg(String, graphql_name='filepath', default=None)),
))
    )


class CreditCard(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('stripe_id', 'space_id', 'brand', 'country', 'name', 'exp_month', 'exp_year', 'last_digits', 'is_default')
    stripe_id = sgqlc.types.Field(String, graphql_name='stripeId')
    space_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='spaceId')
    brand = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='brand')
    country = sgqlc.types.Field(String, graphql_name='country')
    name = sgqlc.types.Field(String, graphql_name='name')
    exp_month = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='expMonth')
    exp_year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='expYear')
    last_digits = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='lastDigits')
    is_default = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isDefault')


class FederatedFile(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'slug', 'creator_id', 'created_in_region', 'space_id', 'date_created', 'last_updated', 'whitelabel', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'comments_count', 'likes_count', 'followers_count', 'score', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'filename', 'mime_type', 'encoding_type', 'size', 's3_size', 'file_last_modified', 'completed', 'cancelled', 'private', 'copy_of_id', 'source', 'author', 'license', 'md5', 'git_hash', 'featured_in', 'creator', 'followers', 'tags', 'comments', 'can_update', 'can_delete', 'parent_slug', 'is_private', 'description', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'title', 'commenters', 'page_views', 'path', 'url', 'permalink', 'upload_url', 'is_copy', 'original_file', 'can_download', 'conversion_scstar', 'conversion_gltftar', 'conversion_gltfdgraph', 'conversion_gltfjson', 'conversion360_gif', 'conversion360_video')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    whitelabel = sgqlc.types.Field(String, graphql_name='whitelabel')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    comments_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentsCount')
    likes_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likesCount')
    followers_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='followersCount')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    filename = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filename')
    mime_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='mimeType')
    encoding_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='encodingType')
    size = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='size')
    s3_size = sgqlc.types.Field(Float, graphql_name='s3Size')
    file_last_modified = sgqlc.types.Field(DateTime, graphql_name='fileLastModified')
    completed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='completed')
    cancelled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='cancelled')
    private = sgqlc.types.Field(Boolean, graphql_name='private')
    copy_of_id = sgqlc.types.Field(Int, graphql_name='copyOfId')
    source = sgqlc.types.Field(String, graphql_name='source')
    author = sgqlc.types.Field(String, graphql_name='author')
    license = sgqlc.types.Field(String, graphql_name='license')
    md5 = sgqlc.types.Field(String, graphql_name='md5')
    git_hash = sgqlc.types.Field(String, graphql_name='gitHash')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    parent_slug = sgqlc.types.Field(String, graphql_name='parentSlug')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    description = sgqlc.types.Field(String, graphql_name='description')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    path = sgqlc.types.Field(String, graphql_name='path')
    url = sgqlc.types.Field(String, graphql_name='url')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    upload_url = sgqlc.types.Field(String, graphql_name='uploadUrl')
    is_copy = sgqlc.types.Field(Boolean, graphql_name='isCopy')
    original_file = sgqlc.types.Field('File', graphql_name='originalFile')
    can_download = sgqlc.types.Field(Boolean, graphql_name='canDownload')
    conversion_scstar = sgqlc.types.Field('FileConversion', graphql_name='conversionScstar')
    conversion_gltftar = sgqlc.types.Field('FileConversion', graphql_name='conversionGltftar')
    conversion_gltfdgraph = sgqlc.types.Field('FileConversion', graphql_name='conversionGltfdgraph')
    conversion_gltfjson = sgqlc.types.Field('FileConversion', graphql_name='conversionGltfjson')
    conversion360_gif = sgqlc.types.Field('FileConversion', graphql_name='conversion360Gif')
    conversion360_video = sgqlc.types.Field('FileConversion', graphql_name='conversion360Video')


class FederatedInitiative(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'slug', 'creator_id', 'created_in_region', 'space_id', 'date_created', 'last_updated', 'whitelabel', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'comments_count', 'likes_count', 'followers_count', 'score', 'pageviews_count', 'public_read', 'registered_read', 'country_code', 'tax_id', 'content_ptr_id', 'avatar_id', 'title', 'description', 'organization_type_id', 'manufacturer', 'prefered_plan_id', 'is_confirmed', 'has_avatar', 'featured_in', 'avatar', 'organization_type', 'prefered_plan', 'creator', 'followers', 'tags', 'comments', 'invite_link', 'invoices', 'billing_subscriptions', 'has_private_projects_subscription', 'has_paid_subscription', 'has_billing_permissions', 'has_valid_payment_method', 'seats_usage', 'subscription_preview', 'credit_cards', 'trial_period_end', 'remaining_shared_files', 'social_accounts', 'forum', 'following_count', 'can_update', 'can_delete', 'parent_slug', 'is_private', 'content', 'parent_content', 'in_space', 'image_fallback_char', 'commenters', 'page_views', 'projects', 'shared_files', 'stories', 'collections', 'groups', 'members', 'projects_count', 'stories_count', 'collections_count', 'threads_count')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    whitelabel = sgqlc.types.Field(String, graphql_name='whitelabel')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    comments_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentsCount')
    likes_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likesCount')
    followers_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='followersCount')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    country_code = sgqlc.types.Field(String, graphql_name='countryCode')
    tax_id = sgqlc.types.Field(String, graphql_name='taxId')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    avatar_id = sgqlc.types.Field(Int, graphql_name='avatarId')
    title = sgqlc.types.Field(String, graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    organization_type_id = sgqlc.types.Field(Int, graphql_name='organizationTypeId')
    manufacturer = sgqlc.types.Field('Manufacturer', graphql_name='manufacturer')
    prefered_plan_id = sgqlc.types.Field(Int, graphql_name='preferedPlanId')
    is_confirmed = sgqlc.types.Field(String, graphql_name='isConfirmed')
    has_avatar = sgqlc.types.Field(String, graphql_name='hasAvatar')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    organization_type = sgqlc.types.Field(OrganizationType, graphql_name='organizationType')
    prefered_plan = sgqlc.types.Field(BillingPlan, graphql_name='preferedPlan')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    invite_link = sgqlc.types.Field('InviteLink', graphql_name='inviteLink')
    invoices = sgqlc.types.Field(sgqlc.types.list_of(BillingInvoice), graphql_name='invoices')
    billing_subscriptions = sgqlc.types.Field(sgqlc.types.list_of(BillingSubscription), graphql_name='billingSubscriptions')
    has_private_projects_subscription = sgqlc.types.Field(Boolean, graphql_name='hasPrivateProjectsSubscription')
    has_paid_subscription = sgqlc.types.Field(Boolean, graphql_name='hasPaidSubscription')
    has_billing_permissions = sgqlc.types.Field(Boolean, graphql_name='hasBillingPermissions')
    has_valid_payment_method = sgqlc.types.Field(Boolean, graphql_name='hasValidPaymentMethod')
    seats_usage = sgqlc.types.Field(SeatsUsage, graphql_name='seatsUsage')
    subscription_preview = sgqlc.types.Field(SubscriptionPreview, graphql_name='subscriptionPreview', args=sgqlc.types.ArgDict((
        ('coupon', sgqlc.types.Arg(String, graphql_name='coupon', default=None)),
        ('extra_seats', sgqlc.types.Arg(Int, graphql_name='extraSeats', default=None)),
))
    )
    credit_cards = sgqlc.types.Field(sgqlc.types.list_of(CreditCard), graphql_name='creditCards')
    trial_period_end = sgqlc.types.Field(DateTime, graphql_name='trialPeriodEnd')
    remaining_shared_files = sgqlc.types.Field(Int, graphql_name='remainingSharedFiles')
    social_accounts = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socialAccounts')
    forum = sgqlc.types.Field('Forum', graphql_name='forum')
    following_count = sgqlc.types.Field(Int, graphql_name='followingCount')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    parent_slug = sgqlc.types.Field(String, graphql_name='parentSlug')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    projects = sgqlc.types.Field(ProjectConnection, graphql_name='projects', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    shared_files = sgqlc.types.Field(SharedFileConnection, graphql_name='sharedFiles', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    stories = sgqlc.types.Field(StoryConnection, graphql_name='stories', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    collections = sgqlc.types.Field(CollectionConnection, graphql_name='collections', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    groups = sgqlc.types.Field(sgqlc.types.list_of('Group'), graphql_name='groups')
    members = sgqlc.types.Field(ProfileConnection, graphql_name='members', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    projects_count = sgqlc.types.Field(Int, graphql_name='projectsCount')
    stories_count = sgqlc.types.Field(Int, graphql_name='storiesCount')
    collections_count = sgqlc.types.Field(Int, graphql_name='collectionsCount')
    threads_count = sgqlc.types.Field(Int, graphql_name='threadsCount')


class File(sgqlc.types.Type, Node, ContentInterface):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'creator_id', 'created_in_region', 'space_id', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'score', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'filename', 'mime_type', 'encoding_type', 'size', 's3_size', 'file_last_modified', 'completed', 'cancelled', 'private', 'copy_of_id', 'source', 'author', 'license', 'md5', 'git_hash', 'featured_in', 'followers', 'tags', 'comments', 'can_update', 'can_delete', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'title', 'commenters', 'page_views', 'path', 'url', 'permalink', 'upload_url', 'is_copy', 'original_file', 'can_download', 'conversion_scstar', 'conversion_gltftar', 'conversion_gltfdgraph', 'conversion_gltfjson', 'conversion360_gif', 'conversion360_video')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    filename = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filename')
    mime_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='mimeType')
    encoding_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='encodingType')
    size = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='size')
    s3_size = sgqlc.types.Field(Float, graphql_name='s3Size')
    file_last_modified = sgqlc.types.Field(DateTime, graphql_name='fileLastModified')
    completed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='completed')
    cancelled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='cancelled')
    private = sgqlc.types.Field(Boolean, graphql_name='private')
    copy_of_id = sgqlc.types.Field(Int, graphql_name='copyOfId')
    source = sgqlc.types.Field(String, graphql_name='source')
    author = sgqlc.types.Field(String, graphql_name='author')
    license = sgqlc.types.Field(String, graphql_name='license')
    md5 = sgqlc.types.Field(String, graphql_name='md5')
    git_hash = sgqlc.types.Field(String, graphql_name='gitHash')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field('File', graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    path = sgqlc.types.Field(String, graphql_name='path')
    url = sgqlc.types.Field(String, graphql_name='url')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    upload_url = sgqlc.types.Field(String, graphql_name='uploadUrl')
    is_copy = sgqlc.types.Field(Boolean, graphql_name='isCopy')
    original_file = sgqlc.types.Field('File', graphql_name='originalFile')
    can_download = sgqlc.types.Field(Boolean, graphql_name='canDownload')
    conversion_scstar = sgqlc.types.Field('FileConversion', graphql_name='conversionScstar')
    conversion_gltftar = sgqlc.types.Field('FileConversion', graphql_name='conversionGltftar')
    conversion_gltfdgraph = sgqlc.types.Field('FileConversion', graphql_name='conversionGltfdgraph')
    conversion_gltfjson = sgqlc.types.Field('FileConversion', graphql_name='conversionGltfjson')
    conversion360_gif = sgqlc.types.Field('FileConversion', graphql_name='conversion360Gif')
    conversion360_video = sgqlc.types.Field('FileConversion', graphql_name='conversion360Video')


class FileConversion(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('viewer_semver', 'conversion_type', 'converted_file_id', 'date_created', 'converted_file', 'status', 'buffers', 'original_file')
    viewer_semver = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='viewerSemver')
    conversion_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='conversionType')
    converted_file_id = sgqlc.types.Field(Int, graphql_name='convertedFileId')
    date_created = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='dateCreated')
    converted_file = sgqlc.types.Field(File, graphql_name='convertedFile')
    status = sgqlc.types.Field(String, graphql_name='status')
    buffers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='buffers')
    original_file = sgqlc.types.Field(File, graphql_name='originalFile')


class Forum(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('space_id', 'description', 'threads_count', 'threads_count_public', 'featured_in', 'categories', 'pinned', 'threads', 'parent_content', 'private_threads_count', 'name', 'is_member')
    space_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='spaceId')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    threads_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='threadsCount')
    threads_count_public = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='threadsCountPublic')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    categories = sgqlc.types.Field(sgqlc.types.list_of(Category), graphql_name='categories')
    pinned = sgqlc.types.Field(sgqlc.types.list_of('Thread'), graphql_name='pinned')
    threads = sgqlc.types.Field(ThreadConnection, graphql_name='threads', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    private_threads_count = sgqlc.types.Field(Int, graphql_name='privateThreadsCount')
    name = sgqlc.types.Field(String, graphql_name='name')
    is_member = sgqlc.types.Field(Boolean, graphql_name='isMember')


class Group(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('permissions', 'name', 'space_id', 'parent_id', 'level', 'space', 'parent', 'children', 'invite_links', 'group_invites', 'members', 'can_update', 'can_delete', 'content', 'can_add_member', 'pending_invites')
    permissions = sgqlc.types.Field(JSONString, graphql_name='permissions')
    name = sgqlc.types.Field(String, graphql_name='name')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    parent_id = sgqlc.types.Field(Int, graphql_name='parentId')
    level = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='level')
    space = sgqlc.types.Field('Space', graphql_name='space')
    parent = sgqlc.types.Field('Group', graphql_name='parent')
    children = sgqlc.types.Field(AutoGroupConnection, graphql_name='children', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    invite_links = sgqlc.types.Field(AutoInviteLinkConnection, graphql_name='inviteLinks', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    group_invites = sgqlc.types.Field(AutoGroupInviteConnection, graphql_name='groupInvites', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    members = sgqlc.types.Field(sgqlc.types.list_of(GroupMember), graphql_name='members')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field(ContentInterface, graphql_name='content')
    can_add_member = sgqlc.types.Field(Boolean, graphql_name='canAddMember')
    pending_invites = sgqlc.types.Field(sgqlc.types.list_of('GroupInvite'), graphql_name='pendingInvites')


class GroupInvite(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('group_id', 'status', 'user_id', 'email', 'inviter_id', 'invite_date', 'info', 'intercom_lead_id', 'group', 'username', 'profile', 'more_invites_requested', 'invites_left', 'group_name', 'group_space_type', 'group_space_private', 'group_space_slug', 'group_slug', 'group_title', 'group_description_snippet', 'group_avatar')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='groupId')
    status = sgqlc.types.Field(String, graphql_name='status')
    user_id = sgqlc.types.Field(Int, graphql_name='userId')
    email = sgqlc.types.Field(String, graphql_name='email')
    inviter_id = sgqlc.types.Field(Int, graphql_name='inviterId')
    invite_date = sgqlc.types.Field(DateTime, graphql_name='inviteDate')
    info = sgqlc.types.Field(JSONString, graphql_name='info')
    intercom_lead_id = sgqlc.types.Field(String, graphql_name='intercomLeadId')
    group = sgqlc.types.Field(Group, graphql_name='group')
    username = sgqlc.types.Field(String, graphql_name='username')
    profile = sgqlc.types.Field('Profile', graphql_name='profile')
    more_invites_requested = sgqlc.types.Field(Boolean, graphql_name='moreInvitesRequested')
    invites_left = sgqlc.types.Field(Int, graphql_name='invitesLeft')
    group_name = sgqlc.types.Field(String, graphql_name='groupName')
    group_space_type = sgqlc.types.Field(String, graphql_name='groupSpaceType')
    group_space_private = sgqlc.types.Field(Boolean, graphql_name='groupSpacePrivate')
    group_space_slug = sgqlc.types.Field(String, graphql_name='groupSpaceSlug')
    group_slug = sgqlc.types.Field(String, graphql_name='groupSlug')
    group_title = sgqlc.types.Field(String, graphql_name='groupTitle')
    group_description_snippet = sgqlc.types.Field(String, graphql_name='groupDescriptionSnippet')
    group_avatar = sgqlc.types.Field(File, graphql_name='groupAvatar')


class Initiative(sgqlc.types.Type, Node, ContentInterface):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'creator_id', 'created_in_region', 'space_id', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'score', 'pageviews_count', 'public_read', 'registered_read', 'country_code', 'tax_id', 'content_ptr_id', 'avatar_id', 'title', 'organization_type_id', 'manufacturer', 'prefered_plan_id', 'is_confirmed', 'has_avatar', 'featured_in', 'avatar', 'organization_type', 'prefered_plan', 'followers', 'tags', 'comments', 'invite_link', 'invoices', 'billing_subscriptions', 'has_private_projects_subscription', 'has_paid_subscription', 'has_billing_permissions', 'has_valid_payment_method', 'seats_usage', 'subscription_preview', 'credit_cards', 'trial_period_end', 'remaining_shared_files', 'social_accounts', 'forum', 'following_count', 'can_update', 'can_delete', 'content', 'parent_content', 'in_space', 'image_fallback_char', 'commenters', 'page_views', 'projects', 'shared_files', 'stories', 'collections', 'groups', 'members', 'projects_count', 'stories_count', 'collections_count', 'threads_count')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    country_code = sgqlc.types.Field(String, graphql_name='countryCode')
    tax_id = sgqlc.types.Field(String, graphql_name='taxId')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    avatar_id = sgqlc.types.Field(Int, graphql_name='avatarId')
    title = sgqlc.types.Field(String, graphql_name='title')
    organization_type_id = sgqlc.types.Field(Int, graphql_name='organizationTypeId')
    manufacturer = sgqlc.types.Field('Manufacturer', graphql_name='manufacturer')
    prefered_plan_id = sgqlc.types.Field(Int, graphql_name='preferedPlanId')
    is_confirmed = sgqlc.types.Field(String, graphql_name='isConfirmed')
    has_avatar = sgqlc.types.Field(String, graphql_name='hasAvatar')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    avatar = sgqlc.types.Field(File, graphql_name='avatar')
    organization_type = sgqlc.types.Field(OrganizationType, graphql_name='organizationType')
    prefered_plan = sgqlc.types.Field(BillingPlan, graphql_name='preferedPlan')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    invite_link = sgqlc.types.Field('InviteLink', graphql_name='inviteLink')
    invoices = sgqlc.types.Field(sgqlc.types.list_of(BillingInvoice), graphql_name='invoices')
    billing_subscriptions = sgqlc.types.Field(sgqlc.types.list_of(BillingSubscription), graphql_name='billingSubscriptions')
    has_private_projects_subscription = sgqlc.types.Field(Boolean, graphql_name='hasPrivateProjectsSubscription')
    has_paid_subscription = sgqlc.types.Field(Boolean, graphql_name='hasPaidSubscription')
    has_billing_permissions = sgqlc.types.Field(Boolean, graphql_name='hasBillingPermissions')
    has_valid_payment_method = sgqlc.types.Field(Boolean, graphql_name='hasValidPaymentMethod')
    seats_usage = sgqlc.types.Field(SeatsUsage, graphql_name='seatsUsage')
    subscription_preview = sgqlc.types.Field(SubscriptionPreview, graphql_name='subscriptionPreview', args=sgqlc.types.ArgDict((
        ('coupon', sgqlc.types.Arg(String, graphql_name='coupon', default=None)),
        ('extra_seats', sgqlc.types.Arg(Int, graphql_name='extraSeats', default=None)),
))
    )
    credit_cards = sgqlc.types.Field(sgqlc.types.list_of(CreditCard), graphql_name='creditCards')
    trial_period_end = sgqlc.types.Field(DateTime, graphql_name='trialPeriodEnd')
    remaining_shared_files = sgqlc.types.Field(Int, graphql_name='remainingSharedFiles')
    social_accounts = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socialAccounts')
    forum = sgqlc.types.Field(Forum, graphql_name='forum')
    following_count = sgqlc.types.Field(Int, graphql_name='followingCount')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    projects = sgqlc.types.Field(ProjectConnection, graphql_name='projects', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    shared_files = sgqlc.types.Field(SharedFileConnection, graphql_name='sharedFiles', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    stories = sgqlc.types.Field(StoryConnection, graphql_name='stories', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    collections = sgqlc.types.Field(CollectionConnection, graphql_name='collections', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    groups = sgqlc.types.Field(sgqlc.types.list_of(Group), graphql_name='groups')
    members = sgqlc.types.Field(ProfileConnection, graphql_name='members', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    projects_count = sgqlc.types.Field(Int, graphql_name='projectsCount')
    stories_count = sgqlc.types.Field(Int, graphql_name='storiesCount')
    collections_count = sgqlc.types.Field(Int, graphql_name='collectionsCount')
    threads_count = sgqlc.types.Field(Int, graphql_name='threadsCount')


class Intermediator(sgqlc.types.Type, Node, Supplier):
    __schema__ = WIF_schema
    __field_names__ = ()


class InviteLink(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('group_id', 'expires_at', 'accepted', 'content', 'url')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='groupId')
    expires_at = sgqlc.types.Field(DateTime, graphql_name='expiresAt')
    accepted = sgqlc.types.Field(sgqlc.types.list_of(GroupMember), graphql_name='accepted')
    content = sgqlc.types.Field(Content, graphql_name='content')
    url = sgqlc.types.Field(String, graphql_name='url')


class Invoice(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('order', 'status', 'amount')
    order = sgqlc.types.Field('Order', graphql_name='order')
    status = sgqlc.types.Field(String, graphql_name='status')
    amount = sgqlc.types.Field(Float, graphql_name='amount')


class InvoicePage(sgqlc.types.Type, Page):
    __schema__ = WIF_schema
    __field_names__ = ()


class Issue(sgqlc.types.Type, Node, ContentInterface):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'creator_id', 'created_in_region', 'space_id', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'score', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'number', 'title', 'description_word_count', 'status', 'project_id', 'can_appear_on_home', 'featured_in', 'project', 'followers', 'tags', 'comments', 'can_update', 'can_delete', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'commenters', 'page_views', 'labels', 'assignees', 'creator_profile', 'can_add_delete_labels')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    number = sgqlc.types.Field(Int, graphql_name='number')
    title = sgqlc.types.Field(String, graphql_name='title')
    description_word_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='descriptionWordCount')
    status = sgqlc.types.Field(String, graphql_name='status')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='projectId')
    can_appear_on_home = sgqlc.types.Field(String, graphql_name='canAppearOnHome')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    project = sgqlc.types.Field('Project', graphql_name='project')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field(File, graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    labels = sgqlc.types.Field(sgqlc.types.list_of('Label'), graphql_name='labels')
    assignees = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='assignees')
    creator_profile = sgqlc.types.Field('Profile', graphql_name='creatorProfile')
    can_add_delete_labels = sgqlc.types.Field(Boolean, graphql_name='canAddDeleteLabels')


class JobSpec(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('customer_space_id', 'build', 'quantity', 'shipping_address', 'quotes')
    customer_space_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='customerSpaceId')
    build = sgqlc.types.Field(sgqlc.types.non_null(Build), graphql_name='build')
    quantity = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='quantity')
    shipping_address = sgqlc.types.Field(Address, graphql_name='shippingAddress')
    quotes = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Quote')), graphql_name='quotes')


class Label(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'color', 'restricted', 'project_id', 'project', 'can_update', 'can_delete', 'can_be_used_by')
    name = sgqlc.types.Field(String, graphql_name='name')
    color = sgqlc.types.Field(String, graphql_name='color')
    restricted = sgqlc.types.Field(Boolean, graphql_name='restricted')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='projectId')
    project = sgqlc.types.Field('Project', graphql_name='project')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    can_be_used_by = sgqlc.types.Field(Boolean, graphql_name='canBeUsedBy')


class LoggedInUser(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('username', 'email', 'locale', 'profile', 'emails_enabled', 'as_space', 'pending_operation_projects', 'pending_invites', 'emails_preferences', 'notification_center', 'is_staff', 'is_superuser', 'flags', 'source')
    username = sgqlc.types.Field(String, graphql_name='username')
    email = sgqlc.types.Field(String, graphql_name='email')
    locale = sgqlc.types.Field(String, graphql_name='locale')
    profile = sgqlc.types.Field('Profile', graphql_name='profile')
    emails_enabled = sgqlc.types.Field(Boolean, graphql_name='emailsEnabled')
    as_space = sgqlc.types.Field(sgqlc.types.list_of('Space'), graphql_name='asSpace')
    pending_operation_projects = sgqlc.types.Field(sgqlc.types.list_of('Project'), graphql_name='pendingOperationProjects')
    pending_invites = sgqlc.types.Field(sgqlc.types.list_of(GroupInvite), graphql_name='pendingInvites')
    emails_preferences = sgqlc.types.Field(sgqlc.types.list_of(EmailType), graphql_name='emailsPreferences')
    notification_center = sgqlc.types.Field(NotificationCenter, graphql_name='notificationCenter')
    is_staff = sgqlc.types.Field(Boolean, graphql_name='isStaff')
    is_superuser = sgqlc.types.Field(Boolean, graphql_name='isSuperuser')
    flags = sgqlc.types.Field(JSONString, graphql_name='flags')
    source = sgqlc.types.Field(String, graphql_name='source')


class Manufacturer(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('initiative', 'space', 'enquiry_email', 'ships_to', 'telephone', 'founding_year', 'address', 'industries', 'num_employees', 'num_machines', 'file_formats', 'case_studies', 'company_type', 'certificates', 'services')
    initiative = sgqlc.types.Field(sgqlc.types.non_null(FederatedInitiative), graphql_name='initiative')
    space = sgqlc.types.Field(sgqlc.types.non_null('Space'), graphql_name='space')
    enquiry_email = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='enquiryEmail')
    ships_to = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='shipsTo')
    telephone = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='telephone')
    founding_year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='foundingYear')
    address = sgqlc.types.Field(sgqlc.types.non_null(Address), graphql_name='address')
    industries = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='industries')
    num_employees = sgqlc.types.Field(Int, graphql_name='numEmployees')
    num_machines = sgqlc.types.Field(Int, graphql_name='numMachines')
    file_formats = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='fileFormats')
    case_studies = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='caseStudies')
    company_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='companyType')
    certificates = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Certificate)), graphql_name='certificates')
    services = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Service')), graphql_name='services')


class ManufacturerPage(sgqlc.types.Type, Page):
    __schema__ = WIF_schema
    __field_names__ = ()


class Material(sgqlc.types.Type, Node, Optionable):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'parent_material', 'child_materials', 'count', 'is_selectable')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    parent_material = sgqlc.types.Field('Material', graphql_name='parentMaterial')
    child_materials = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Material')), graphql_name='childMaterials', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(MaterialFilter, graphql_name='filter', default=None)),
))
    )
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(MaterialFilter, graphql_name='filter', default=None)),
))
    )
    is_selectable = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isSelectable')


class Message(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('message_type', 'body', 'edited', 'context_id', 'created_by', 'reference_id', 'resource_id', 'timestamp', 'temp_key')
    message_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='messageType')
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='body')
    edited = sgqlc.types.Field(Boolean, graphql_name='edited')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextId')
    created_by = sgqlc.types.Field(String, graphql_name='createdBy')
    reference_id = sgqlc.types.Field(String, graphql_name='referenceId')
    resource_id = sgqlc.types.Field(String, graphql_name='resourceId')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='timestamp')
    temp_key = sgqlc.types.Field(String, graphql_name='tempKey')


class MessagePage(sgqlc.types.Type, Page):
    __schema__ = WIF_schema
    __field_names__ = ()


class MinMaxOption(sgqlc.types.Type, Node, Option):
    __schema__ = WIF_schema
    __field_names__ = ('type', 'step')
    type = sgqlc.types.Field(sgqlc.types.non_null(MinMaxType), graphql_name='type')
    step = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='step')


class OptionInstance(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('option', 'manufacturer', 'for_material', 'for_process', 'value_int', 'value_float', 'value_string', 'value_bool')
    option = sgqlc.types.Field(sgqlc.types.non_null(Option), graphql_name='option')
    manufacturer = sgqlc.types.Field(sgqlc.types.non_null(Manufacturer), graphql_name='manufacturer')
    for_material = sgqlc.types.Field(Material, graphql_name='ForMaterial')
    for_process = sgqlc.types.Field('Process', graphql_name='ForProcess')
    value_int = sgqlc.types.Field(Int, graphql_name='valueInt')
    value_float = sgqlc.types.Field(Float, graphql_name='valueFloat')
    value_string = sgqlc.types.Field(String, graphql_name='valueString')
    value_bool = sgqlc.types.Field(Boolean, graphql_name='valueBool')


class Order(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('quote', 'payment_status', 'order_status', 'confirmation', 'created_at')
    quote = sgqlc.types.Field('Quote', graphql_name='quote')
    payment_status = sgqlc.types.Field(PaymentStatus, graphql_name='paymentStatus')
    order_status = sgqlc.types.Field(OrderStatus, graphql_name='orderStatus')
    confirmation = sgqlc.types.Field(Confirmation, graphql_name='confirmation')
    created_at = sgqlc.types.Field(Time, graphql_name='createdAt')


class OrderPage(sgqlc.types.Type, Page):
    __schema__ = WIF_schema
    __field_names__ = ()


class Part(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'cad_id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    cad_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cadId')


class Post(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'slug', 'creator_id', 'created_in_region', 'space_id', 'date_created', 'last_updated', 'whitelabel', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'comments_count', 'likes_count', 'followers_count', 'score', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'title', 'msg', 'source', 'url', 'forum_id', 'category_id', 'members_only', 'upvote_count', 'featured_in', 'creator', 'followers', 'tags', 'upvotes', 'comments', 'can_update', 'can_delete', 'parent_slug', 'is_private', 'description', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'commenters', 'page_views', 'is_upvoted', 'creator_profile')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    date_created = sgqlc.types.Field(DateTime, graphql_name='dateCreated')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    whitelabel = sgqlc.types.Field(String, graphql_name='whitelabel')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    comments_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentsCount')
    likes_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likesCount')
    followers_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='followersCount')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    title = sgqlc.types.Field(String, graphql_name='title')
    msg = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='msg')
    source = sgqlc.types.Field(String, graphql_name='source')
    url = sgqlc.types.Field(String, graphql_name='url')
    forum_id = sgqlc.types.Field(Float, graphql_name='forumId')
    category_id = sgqlc.types.Field(Float, graphql_name='categoryId')
    members_only = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='membersOnly')
    upvote_count = sgqlc.types.Field(Int, graphql_name='upvoteCount')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    upvotes = sgqlc.types.Field(sgqlc.types.list_of('Upvote'), graphql_name='upvotes')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    parent_slug = sgqlc.types.Field(String, graphql_name='parentSlug')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    description = sgqlc.types.Field(String, graphql_name='description')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field(File, graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    is_upvoted = sgqlc.types.Field(Boolean, graphql_name='isUpvoted')
    creator_profile = sgqlc.types.Field('Profile', graphql_name='creatorProfile')


class Process(sgqlc.types.Type, Node, Optionable):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'parent_process', 'child_processes', 'count', 'is_selectable')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    parent_process = sgqlc.types.Field('Process', graphql_name='parentProcess')
    child_processes = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Process')), graphql_name='childProcesses', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ProcessFilter, graphql_name='filter', default=None)),
))
    )
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ProcessFilter, graphql_name='filter', default=None)),
))
    )
    is_selectable = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isSelectable')


class Profile(sgqlc.types.Type, Node, ContentInterface):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'creator_id', 'created_in_region', 'space_id', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'score', 'pageviews_count', 'public_read', 'registered_read', 'country_code', 'tax_id', 'content_ptr_id', 'avatar_id', 'bio', 'preferred_name', 'user_type_id', 'intent_id', 'user_id', 'prefered_plan_id', 'is_confirmed', 'has_avatar', 'has_bio', 'featured_in', 'avatar', 'user_type', 'intent', 'user', 'prefered_plan', 'followers', 'tags', 'comments', 'invoices', 'billing_subscriptions', 'has_private_projects_subscription', 'has_paid_subscription', 'has_billing_permissions', 'has_valid_payment_method', 'seats_usage', 'subscription_preview', 'credit_cards', 'trial_period_end', 'remaining_shared_files', 'social_accounts', 'forum', 'following_count', 'can_update', 'can_delete', 'content', 'parent_content', 'in_space', 'image_fallback_char', 'title', 'commenters', 'page_views', 'management', 'username', 'email', 'full_name', 'locale', 'invites_left', 'profile_confirmed', 'skills', 'initiatives', 'projects', 'shared_files', 'threads', 'stories', 'collections', 'contributions', 'following_profiles', 'following_initiatives', 'following_channels', 'following_projects', 'contributed_projects', 'teams', 'projects_count', 'stories_count', 'collections_count')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    country_code = sgqlc.types.Field(String, graphql_name='countryCode')
    tax_id = sgqlc.types.Field(String, graphql_name='taxId')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    avatar_id = sgqlc.types.Field(Int, graphql_name='avatarId')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    preferred_name = sgqlc.types.Field(String, graphql_name='preferredName')
    user_type_id = sgqlc.types.Field(Int, graphql_name='userTypeId')
    intent_id = sgqlc.types.Field(Int, graphql_name='intentId')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    prefered_plan_id = sgqlc.types.Field(Int, graphql_name='preferedPlanId')
    is_confirmed = sgqlc.types.Field(String, graphql_name='isConfirmed')
    has_avatar = sgqlc.types.Field(String, graphql_name='hasAvatar')
    has_bio = sgqlc.types.Field(String, graphql_name='hasBio')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    avatar = sgqlc.types.Field(File, graphql_name='avatar')
    user_type = sgqlc.types.Field(ProfileUserType, graphql_name='userType')
    intent = sgqlc.types.Field(ProfileIntent, graphql_name='intent')
    user = sgqlc.types.Field('User', graphql_name='user')
    prefered_plan = sgqlc.types.Field(BillingPlan, graphql_name='preferedPlan')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    invoices = sgqlc.types.Field(sgqlc.types.list_of(BillingInvoice), graphql_name='invoices')
    billing_subscriptions = sgqlc.types.Field(sgqlc.types.list_of(BillingSubscription), graphql_name='billingSubscriptions')
    has_private_projects_subscription = sgqlc.types.Field(Boolean, graphql_name='hasPrivateProjectsSubscription')
    has_paid_subscription = sgqlc.types.Field(Boolean, graphql_name='hasPaidSubscription')
    has_billing_permissions = sgqlc.types.Field(Boolean, graphql_name='hasBillingPermissions')
    has_valid_payment_method = sgqlc.types.Field(Boolean, graphql_name='hasValidPaymentMethod')
    seats_usage = sgqlc.types.Field(SeatsUsage, graphql_name='seatsUsage')
    subscription_preview = sgqlc.types.Field(SubscriptionPreview, graphql_name='subscriptionPreview', args=sgqlc.types.ArgDict((
        ('coupon', sgqlc.types.Arg(String, graphql_name='coupon', default=None)),
        ('extra_seats', sgqlc.types.Arg(Int, graphql_name='extraSeats', default=None)),
))
    )
    credit_cards = sgqlc.types.Field(sgqlc.types.list_of(CreditCard), graphql_name='creditCards')
    trial_period_end = sgqlc.types.Field(DateTime, graphql_name='trialPeriodEnd')
    remaining_shared_files = sgqlc.types.Field(Int, graphql_name='remainingSharedFiles')
    social_accounts = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socialAccounts')
    forum = sgqlc.types.Field(Forum, graphql_name='forum')
    following_count = sgqlc.types.Field(Int, graphql_name='followingCount')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    commenters = sgqlc.types.Field(sgqlc.types.list_of('Profile'), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    management = sgqlc.types.Field(JSONString, graphql_name='management')
    username = sgqlc.types.Field(String, graphql_name='username')
    email = sgqlc.types.Field(String, graphql_name='email')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    locale = sgqlc.types.Field(String, graphql_name='locale')
    invites_left = sgqlc.types.Field(Int, graphql_name='invitesLeft')
    profile_confirmed = sgqlc.types.Field(Boolean, graphql_name='profileConfirmed')
    skills = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='skills')
    initiatives = sgqlc.types.Field(InitiativeConnection, graphql_name='initiatives', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    projects = sgqlc.types.Field(ProjectConnection, graphql_name='projects', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    shared_files = sgqlc.types.Field(SharedFileConnection, graphql_name='sharedFiles', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    threads = sgqlc.types.Field(ThreadConnection, graphql_name='threads', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    stories = sgqlc.types.Field(StoryConnection, graphql_name='stories', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    collections = sgqlc.types.Field(CollectionConnection, graphql_name='collections', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    contributions = sgqlc.types.Field(ContributionConnection, graphql_name='contributions', args=sgqlc.types.ArgDict((
        ('project_id', sgqlc.types.Arg(ID, graphql_name='projectId', default=None)),
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    following_profiles = sgqlc.types.Field(ProfileConnection, graphql_name='followingProfiles', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    following_initiatives = sgqlc.types.Field(InitiativeConnection, graphql_name='followingInitiatives', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    following_channels = sgqlc.types.Field(ChannelConnection, graphql_name='followingChannels', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    following_projects = sgqlc.types.Field(ProjectConnection, graphql_name='followingProjects', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    contributed_projects = sgqlc.types.Field(ProjectConnection, graphql_name='contributedProjects', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    teams = sgqlc.types.Field(sgqlc.types.list_of(GroupMember), graphql_name='teams')
    projects_count = sgqlc.types.Field(Int, graphql_name='projectsCount')
    stories_count = sgqlc.types.Field(Int, graphql_name='storiesCount')
    collections_count = sgqlc.types.Field(Int, graphql_name='collectionsCount')


class Project(sgqlc.types.Type, Node, ContentInterface):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'creator_id', 'created_in_region', 'space_id', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'score', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'name', 'image_id', 'license', 'contribution_count', 'archive_download_count', 'context_id', 'project_type', 'import_status', 'import_job_id', 'slack_thread_ts', 'slack_contribution_thread_ts', 'is_exact_fork_copy', 'has_image', 'star_count', 'head_contribution', 'can_appear_on_home', 'has_contributions', 'featured_in', 'image', 'phase', 'context', 'followers', 'tags', 'collections', 'comments', 'contributions', 'invite_link', 'social_accounts', 'forum', 'following_count', 'can_update', 'can_delete', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'title', 'commenters', 'page_views', 'description_snippet', 'private', 'forked_from', 'pending_operations', 'conflicts', 'conflicts_parent', 'contribution_upstream', 'last_zip_generated', 'tracker', 'creator_profile', 'is_starred', 'fork_count', 'contribution', 'contributors', 'file_history')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    name = sgqlc.types.Field(String, graphql_name='name')
    image_id = sgqlc.types.Field(Int, graphql_name='imageId')
    license = sgqlc.types.Field(License, graphql_name='license')
    contribution_count = sgqlc.types.Field(Int, graphql_name='contributionCount')
    archive_download_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='archiveDownloadCount')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='contextId')
    project_type = sgqlc.types.Field(sgqlc.types.non_null(project_type), graphql_name='projectType')
    import_status = sgqlc.types.Field(ImportStatus, graphql_name='importStatus')
    import_job_id = sgqlc.types.Field(String, graphql_name='importJobId')
    slack_thread_ts = sgqlc.types.Field(String, graphql_name='slackThreadTs')
    slack_contribution_thread_ts = sgqlc.types.Field(sgqlc.types.non_null(JSONString), graphql_name='slackContributionThreadTs')
    is_exact_fork_copy = sgqlc.types.Field(String, graphql_name='isExactForkCopy')
    has_image = sgqlc.types.Field(String, graphql_name='hasImage')
    star_count = sgqlc.types.Field(Int, graphql_name='starCount')
    head_contribution = sgqlc.types.Field(String, graphql_name='headContribution')
    can_appear_on_home = sgqlc.types.Field(String, graphql_name='canAppearOnHome')
    has_contributions = sgqlc.types.Field(String, graphql_name='hasContributions')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    image = sgqlc.types.Field(File, graphql_name='image')
    phase = sgqlc.types.Field(ProjectPhase, graphql_name='phase')
    context = sgqlc.types.Field(Context, graphql_name='context')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    collections = sgqlc.types.Field(sgqlc.types.list_of(Collection), graphql_name='collections')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    contributions = sgqlc.types.Field(ContributionConnection, graphql_name='contributions', args=sgqlc.types.ArgDict((
        ('project_id', sgqlc.types.Arg(ID, graphql_name='projectId', default=None)),
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    invite_link = sgqlc.types.Field(InviteLink, graphql_name='inviteLink')
    social_accounts = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socialAccounts')
    forum = sgqlc.types.Field(Forum, graphql_name='forum')
    following_count = sgqlc.types.Field(Int, graphql_name='followingCount')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    avatar = sgqlc.types.Field(File, graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    title = sgqlc.types.Field(String, graphql_name='title')
    commenters = sgqlc.types.Field(sgqlc.types.list_of(Profile), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    description_snippet = sgqlc.types.Field(String, graphql_name='descriptionSnippet')
    private = sgqlc.types.Field(Boolean, graphql_name='private')
    forked_from = sgqlc.types.Field(DiffInfo, graphql_name='forkedFrom')
    pending_operations = sgqlc.types.Field(sgqlc.types.list_of(ContribOp), graphql_name='pendingOperations')
    conflicts = sgqlc.types.Field(sgqlc.types.list_of(Conflict), graphql_name='conflicts')
    conflicts_parent = sgqlc.types.Field(String, graphql_name='conflictsParent')
    contribution_upstream = sgqlc.types.Field(Contribution, graphql_name='contributionUpstream')
    last_zip_generated = sgqlc.types.Field(Boolean, graphql_name='lastZipGenerated')
    tracker = sgqlc.types.Field('Tracker', graphql_name='tracker')
    creator_profile = sgqlc.types.Field(Profile, graphql_name='creatorProfile')
    is_starred = sgqlc.types.Field(Boolean, graphql_name='isStarred')
    fork_count = sgqlc.types.Field(Int, graphql_name='forkCount')
    contribution = sgqlc.types.Field(Contribution, graphql_name='contribution', args=sgqlc.types.ArgDict((
        ('version', sgqlc.types.Arg(String, graphql_name='version', default=None)),
))
    )
    contributors = sgqlc.types.Field(ProfileConnection, graphql_name='contributors', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    file_history = sgqlc.types.Field(OpsConnection, graphql_name='fileHistory', args=sgqlc.types.ArgDict((
        ('uuid', sgqlc.types.Arg(String, graphql_name='uuid', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class Quote(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('job_spec', 'process', 'material', 'service_instance', 'cost', 'currency', 'valid_until', 'orders', 'reject_reason', 'reject_description', 'proposed_lead_time', 'notes', 'shipping', 'is_shipping_included', 'is_estimated', 'is_invalid', 'created_by', 'created_at')
    job_spec = sgqlc.types.Field(sgqlc.types.non_null(JobSpec), graphql_name='jobSpec')
    process = sgqlc.types.Field(sgqlc.types.non_null(Process), graphql_name='process')
    material = sgqlc.types.Field(sgqlc.types.non_null(Material), graphql_name='material')
    service_instance = sgqlc.types.Field('ServiceInstance', graphql_name='serviceInstance')
    cost = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='cost')
    currency = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='currency')
    valid_until = sgqlc.types.Field(sgqlc.types.non_null(Time), graphql_name='validUntil')
    orders = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Order)), graphql_name='orders')
    reject_reason = sgqlc.types.Field(String, graphql_name='rejectReason')
    reject_description = sgqlc.types.Field(String, graphql_name='rejectDescription')
    proposed_lead_time = sgqlc.types.Field(Time, graphql_name='proposedLeadTime')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    shipping = sgqlc.types.Field('Shipping', graphql_name='shipping')
    is_shipping_included = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isShippingIncluded')
    is_estimated = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isEstimated')
    is_invalid = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isInvalid')
    created_by = sgqlc.types.Field(sgqlc.types.non_null(Supplier), graphql_name='createdBy')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Time), graphql_name='createdAt')


class QuotePage(sgqlc.types.Type, Page):
    __schema__ = WIF_schema
    __field_names__ = ()


class RequestForQuote(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('state', 'type', 'job_spec', 'intermediator_session', 'sessions', 'quoting_priority', 'quoting_priority_description', 'quotes_needed_by', 'estimated_award_date', 'customer_space', 'created_at')
    state = sgqlc.types.Field(sgqlc.types.non_null(RequestForQuoteState), graphql_name='state')
    type = sgqlc.types.Field(sgqlc.types.non_null(RequestForQuoteType), graphql_name='type')
    job_spec = sgqlc.types.Field(sgqlc.types.non_null(JobSpec), graphql_name='jobSpec')
    intermediator_session = sgqlc.types.Field('Session', graphql_name='intermediatorSession')
    sessions = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Session')), graphql_name='sessions')
    quoting_priority = sgqlc.types.Field(QuotingPriority, graphql_name='quotingPriority')
    quoting_priority_description = sgqlc.types.Field(String, graphql_name='quotingPriorityDescription')
    quotes_needed_by = sgqlc.types.Field(Time, graphql_name='quotesNeededBy')
    estimated_award_date = sgqlc.types.Field(Time, graphql_name='estimatedAwardDate')
    customer_space = sgqlc.types.Field(sgqlc.types.non_null('Space'), graphql_name='customerSpace')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Time), graphql_name='createdAt')


class RequestForQuotePage(sgqlc.types.Type, Page):
    __schema__ = WIF_schema
    __field_names__ = ()


class SelectionOption(sgqlc.types.Type, Node, Option):
    __schema__ = WIF_schema
    __field_names__ = ('order',)
    order = sgqlc.types.Field(String, graphql_name='order')


class Service(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('is_active', 'process', 'material')
    is_active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isActive')
    process = sgqlc.types.Field(sgqlc.types.non_null(Process), graphql_name='process')
    material = sgqlc.types.Field(sgqlc.types.non_null(Material), graphql_name='material')


class ServiceInstance(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('is_archived', 'service', 'manufacturer')
    is_archived = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isArchived')
    service = sgqlc.types.Field(sgqlc.types.non_null(Service), graphql_name='service')
    manufacturer = sgqlc.types.Field(sgqlc.types.non_null(Manufacturer), graphql_name='manufacturer')


class ServicePage(sgqlc.types.Type, Page):
    __schema__ = WIF_schema
    __field_names__ = ()


class Session(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('supplier', 'state', 'request_for_quote', 'job_specs', 'share_file', 'created_at')
    supplier = sgqlc.types.Field(sgqlc.types.non_null(Supplier), graphql_name='supplier')
    state = sgqlc.types.Field(sgqlc.types.non_null(SessionState), graphql_name='state')
    request_for_quote = sgqlc.types.Field(sgqlc.types.non_null(RequestForQuote), graphql_name='requestForQuote')
    job_specs = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(JobSpec)), graphql_name='jobSpecs')
    share_file = sgqlc.types.Field(sgqlc.types.non_null('SharedFile'), graphql_name='shareFile')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Time), graphql_name='createdAt')


class SessionPage(sgqlc.types.Type, Page):
    __schema__ = WIF_schema
    __field_names__ = ()


class SharedFile(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('name', 'revision', 'revisions', 'groups', 'creator', 'context', 'space', 'in_space', 'can_update', 'can_delete', 'is_private', 'slug')
    name = sgqlc.types.Field(String, graphql_name='name')
    revision = sgqlc.types.Field(SharedFileRevision, graphql_name='revision')
    revisions = sgqlc.types.Field(SharedFileRevisionConnection, graphql_name='revisions', args=sgqlc.types.ArgDict((
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    groups = sgqlc.types.Field(sgqlc.types.list_of(Group), graphql_name='groups')
    creator = sgqlc.types.Field('User', graphql_name='creator')
    context = sgqlc.types.Field(Context, graphql_name='context')
    space = sgqlc.types.Field('Space', graphql_name='space')
    in_space = sgqlc.types.Field('Space', graphql_name='inSpace')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    slug = sgqlc.types.Field(String, graphql_name='slug')


class Shipping(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('currency', 'cost', 'delivery_estimate', 'provider', 'tracking_number')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    cost = sgqlc.types.Field(Float, graphql_name='cost')
    delivery_estimate = sgqlc.types.Field(Time, graphql_name='deliveryEstimate')
    provider = sgqlc.types.Field(String, graphql_name='provider')
    tracking_number = sgqlc.types.Field(String, graphql_name='trackingNumber')


class Skill(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('content', 'display_name', 'skill_type')
    content = sgqlc.types.Field(String, graphql_name='content')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    skill_type = sgqlc.types.Field(String, graphql_name='skillType')


class Social(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('account_name', 'account_type')
    account_name = sgqlc.types.Field(String, graphql_name='accountName')
    account_type = sgqlc.types.Field(String, graphql_name='accountType')


class Space(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('parent', 'content', 'space_type', 'has_private_projects_subscription', 'has_paid_subscription', 'has_billing_permissions', 'has_valid_payment_method', 'trial_period_end', 'remaining_shared_files', 'which_types')
    parent = sgqlc.types.Field('Space', graphql_name='parent')
    content = sgqlc.types.Field(Content, graphql_name='content')
    space_type = sgqlc.types.Field(String, graphql_name='spaceType')
    has_private_projects_subscription = sgqlc.types.Field(Boolean, graphql_name='hasPrivateProjectsSubscription')
    has_paid_subscription = sgqlc.types.Field(Boolean, graphql_name='hasPaidSubscription')
    has_billing_permissions = sgqlc.types.Field(Boolean, graphql_name='hasBillingPermissions')
    has_valid_payment_method = sgqlc.types.Field(Boolean, graphql_name='hasValidPaymentMethod')
    trial_period_end = sgqlc.types.Field(DateTime, graphql_name='trialPeriodEnd')
    remaining_shared_files = sgqlc.types.Field(Int, graphql_name='remainingSharedFiles')
    which_types = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='whichTypes')


class Story(sgqlc.types.Type, Node, ContentInterface):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'creator_id', 'created_in_region', 'space_id', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'score', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'avatar_id', 'title', 'body', 'body_word_count', 'can_appear_on_home', 'featured_in', 'avatar', 'followers', 'tags', 'comments', 'can_update', 'can_delete', 'content', 'parent_content', 'in_space', 'image_fallback_char', 'commenters', 'page_views', 'body_snippet', 'read_length', 'creator_profile')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='score')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    avatar_id = sgqlc.types.Field(Int, graphql_name='avatarId')
    title = sgqlc.types.Field(String, graphql_name='title')
    body = sgqlc.types.Field(String, graphql_name='body')
    body_word_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='bodyWordCount')
    can_appear_on_home = sgqlc.types.Field(String, graphql_name='canAppearOnHome')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    avatar = sgqlc.types.Field(File, graphql_name='avatar')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field(Space, graphql_name='inSpace')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    commenters = sgqlc.types.Field(sgqlc.types.list_of(Profile), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    body_snippet = sgqlc.types.Field(String, graphql_name='bodySnippet')
    read_length = sgqlc.types.Field(Int, graphql_name='readLength')
    creator_profile = sgqlc.types.Field(Profile, graphql_name='creatorProfile')


class Tag(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class Thread(sgqlc.types.Type, Node, ContentInterface):
    __schema__ = WIF_schema
    __field_names__ = ('featured_in', 'type', 'creator_id', 'created_in_region', 'space_id', 'white_label_only_content', 'last_commented_at', 'last_activity_at', 'pageviews_count', 'public_read', 'registered_read', 'content_ptr_id', 'title', 'msg', 'forum_id', 'category_id', 'members_only', 'upvote_count', 'featured_in', 'forum', 'category', 'followers', 'tags', 'comments', 'url_id', 'can_update', 'can_delete', 'content', 'parent_content', 'in_space', 'avatar', 'image_fallback_char', 'commenters', 'page_views', 'is_pinned', 'can_pin', 'creator_profile')
    featured_in = sgqlc.types.Field(String, graphql_name='FeaturedIn')
    type = sgqlc.types.Field(String, graphql_name='type')
    creator_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='creatorId')
    created_in_region = sgqlc.types.Field(String, graphql_name='createdInRegion')
    space_id = sgqlc.types.Field(Int, graphql_name='spaceId')
    white_label_only_content = sgqlc.types.Field(Boolean, graphql_name='whiteLabelOnlyContent')
    last_commented_at = sgqlc.types.Field(DateTime, graphql_name='lastCommentedAt')
    last_activity_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastActivityAt')
    pageviews_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageviewsCount')
    public_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='publicRead')
    registered_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='registeredRead')
    content_ptr_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentPtrId')
    title = sgqlc.types.Field(String, graphql_name='title')
    msg = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='msg')
    forum_id = sgqlc.types.Field(Float, graphql_name='forumId')
    category_id = sgqlc.types.Field(String, graphql_name='categoryId')
    members_only = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='membersOnly')
    upvote_count = sgqlc.types.Field(String, graphql_name='upvoteCount')
    featured_in = sgqlc.types.Field(String, graphql_name='featuredIn')
    forum = sgqlc.types.Field(Forum, graphql_name='forum')
    category = sgqlc.types.Field(Category, graphql_name='category')
    followers = sgqlc.types.Field(ProfileConnection, graphql_name='followers', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of(Tag), graphql_name='tags')
    comments = sgqlc.types.Field(CommentConnection, graphql_name='comments', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('origin', sgqlc.types.Arg(ID, graphql_name='origin', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    url_id = sgqlc.types.Field(String, graphql_name='urlId')
    can_update = sgqlc.types.Field(Boolean, graphql_name='canUpdate')
    can_delete = sgqlc.types.Field(Boolean, graphql_name='canDelete')
    content = sgqlc.types.Field(Content, graphql_name='content')
    parent_content = sgqlc.types.Field(Content, graphql_name='parentContent')
    in_space = sgqlc.types.Field(Space, graphql_name='inSpace')
    avatar = sgqlc.types.Field(File, graphql_name='avatar')
    image_fallback_char = sgqlc.types.Field(String, graphql_name='imageFallbackChar')
    commenters = sgqlc.types.Field(sgqlc.types.list_of(Profile), graphql_name='commenters')
    page_views = sgqlc.types.Field(Int, graphql_name='pageViews')
    is_pinned = sgqlc.types.Field(Boolean, graphql_name='isPinned')
    can_pin = sgqlc.types.Field(Boolean, graphql_name='canPin')
    creator_profile = sgqlc.types.Field(Profile, graphql_name='creatorProfile')


class Tracker(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('issues', 'issue', 'labels')
    issues = sgqlc.types.Field(IssueConnection, graphql_name='issues', args=sgqlc.types.ArgDict((
        ('sort_by', sgqlc.types.Arg(String, graphql_name='sortBy', default=None)),
        ('filter_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='filterBy', default=None)),
        ('contains', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='contains', default=None)),
        ('not_contains', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name='notContains', default=None)),
        ('whitelabels', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='whitelabels', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    issue = sgqlc.types.Field(Issue, graphql_name='issue', args=sgqlc.types.ArgDict((
        ('issue_slug', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='issueSlug', default=None)),
))
    )
    labels = sgqlc.types.Field(sgqlc.types.list_of(Label), graphql_name='labels')


class Upvote(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('user_id', 'post_id', 'date_created', 'user', 'post')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    post_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='postId')
    date_created = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='dateCreated')
    user = sgqlc.types.Field('User', graphql_name='user')
    post = sgqlc.types.Field(Post, graphql_name='post')


class User(sgqlc.types.Type, Node):
    __schema__ = WIF_schema
    __field_names__ = ('username', 'email', 'locale', 'profile', 'emails_enabled', 'as_space')
    username = sgqlc.types.Field(String, graphql_name='username')
    email = sgqlc.types.Field(String, graphql_name='email')
    locale = sgqlc.types.Field(String, graphql_name='locale')
    profile = sgqlc.types.Field(Profile, graphql_name='profile')
    emails_enabled = sgqlc.types.Field(Boolean, graphql_name='emailsEnabled')
    as_space = sgqlc.types.Field(sgqlc.types.list_of(Space), graphql_name='asSpace')



########################################################################
# Unions
########################################################################
class NotificationTarget(sgqlc.types.Union):
    __schema__ = WIF_schema
    __types__ = (Contribution, Project, Story, Profile, Thread, Initiative, Comment, Issue, GroupInvite, HTMLNotification)



########################################################################
# Schema Entry Points
########################################################################
WIF_schema.query_type = Query
WIF_schema.mutation_type = Mutation
WIF_schema.subscription_type = None

