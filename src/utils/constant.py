import enum

class ConsentType(str, enum.Enum):
    TERMS_OF_SERVICE = "terms_of_service"
    PRIVACY_POLICY = "privacy_policy"
    MARKETING = "marketing"
    DATA_SHARING = "data_sharing"
    THIRD_PARTY_SHARING = "third_party_sharing"
