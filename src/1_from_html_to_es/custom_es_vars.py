def es_vars(var):
    if var == "mapping_rev":
        return """
        {
            "properties":
            {
                "businessUnit":
                {
                    "properties":
                    {
                        "id":
                        {
                            "type": "keyword"
                        }
                    }
                },
                "reviews":
                {
                    "properties":
                    {
                        "consumer.countryCode":
                        {
                            "type": "keyword"
                        },
                        "consumer.displayName":
                        {
                            "type": "keyword"
                        },
                        "consumer.imageUrl":
                        {
                            "type": "keyword"
                        },
                        "consumer.numberOfReviews":
                        {
                            "type": "integer"
                        },
                        "consumer.hasImage":
                        {
                            "type": "boolean"
                        },
                        "consumer.isVerified":
                        {
                            "type": "boolean"
                        },
                        "consumer.id":
                        {
                            "type": "keyword"
                        },
                        "consumersReviewCountOnSameDomain":
                        {
                            "type": "integer"
                        },
                        "dates.experiencedDate":
                        {
                            "type": "date"
                        },
                        "dates.publishedDate":
                        {
                            "type": "keyword"
                        },
                        "dates.updatedDate":
                        {
                            "type": "keyword"
                        },
                        "filtered":
                        {
                            "type": "boolean"
                        },
                        "hasUnhandledReports":
                        {
                            "type": "boolean"
                        },
                        "id":
                        {
                            "type": "keyword"
                        },
                        "labels.merged":
                        {
                            "type": "keyword"
                        },
                        "labels.verification.isVerified":
                        {
                            "type": "boolean"
                        },
                        "labels.verification.createdDateTime":
                        {
                            "type": "date"
                        },
                        "labels.verification.reviewSourceName":
                        {
                            "type": "keyword"
                        },
                        "labels.verification.verificationSource":
                        {
                            "type": "keyword"
                        },
                        "labels.verification.verificationLevel":
                        {
                            "type": "keyword"
                        },
                        "language":
                        {
                            "type": "keyword"
                        },
                        "likes":
                        {
                            "type": "long"
                        },
                        "pending":
                        {
                            "type": "boolean"
                        },
                        "rating":
                        {
                            "type": "short"
                        },
                        "reply.message":
                        {
                            "type": "text"
                        },
                        "reply.publishedDate":
                        {
                            "type": "date"
                        },
                        "reply.updatedDate":
                        {
                            "type": "date"
                        },
                        "text":
                        {
                            "type": "text"
                        },
                        "title":
                        {
                            "type": "text"
                        }
                    }
                }
            }
        }
        """

    elif var == "mapping_comp":
        return """
        {
            "properties":
            {
                "businesses":
                {
                    "properties":
                    {
                        "businessUnitId":
                        {
                            "type": "keyword"
                        },
                        "categories.categoryId":
                        {
                            "type": "keyword"
                        },
                        "categories.displayName":
                        {
                            "type": "keyword"
                        },
                        "categories.isPredicted":
                        {
                            "type": "boolean"
                        },
                        "contact.website":
                        {
                            "type": "keyword"
                        },
                        "contact.email":
                        {
                            "type": "keyword"
                        },
                        "contact.phone":
                        {
                            "type": "keyword"
                        },
                        "displayName":
                        {
                            "type": "keyword"
                        },
                        "identifyingName":
                        {
                            "type": "keyword"
                        },
                        "isRecommendedInCategories":
                        {
                            "type": "boolean"
                        },
                        "location.address":
                        {
                            "type": "text"
                        },
                        "location.city":
                        {
                            "type": "keyword"
                        },
                        "location.zipCode":
                        {
                            "type": "keyword"
                        },
                        "location.country":
                        {
                            "type": "keyword"
                        },
                        "logoUrl":
                        {
                            "type": "keyword"
                        },
                        "numberOfReviews":
                        {
                            "type": "long"
                        },
                        "stars":
                        {
                            "type": "long"
                        },
                        "trustScore":
                        {
                            "type": "float"
                        }
                    }
                }
            }
        }
        """


    elif var == "mapping_cat":
        return """
        {
            "properties":
            {
                "subCategories":
                {
                    "properties":
                    {
                        "food_beverages_tobacco":
                        {
                            "type": "flattened"
                        },
                        "animals_pets":
                        {
                            "type": "flattened"
                        },
                        "money_insurance":
                        {
                            "type": "flattened"
                        },
                        "beauty_wellbeing":
                        {
                            "type": "flattened"
                        },
                        "construction_manufactoring":
                        {
                            "type": "flattened"
                        },
                        "education_training":
                        {
                            "type": "flattened"
                        },
                        "electronics_technology":
                        {
                            "type": "flattened"
                        },
                        "events_entertainment":
                        {
                            "type": "flattened"
                        },
                        "hobbies_crafts":
                        {
                            "type": "flattened"
                        },
                        "home_garden":
                        {
                            "type": "flattened"
                        },
                        "media_publishing":
                        {
                            "type": "flattened"
                        },
                        "restaurants_bars":
                        {
                            "type": "flattened"
                        },
                        "health_medical":
                        {
                            "type": "flattened"
                        },
                        "utilities":
                        {
                            "type": "flattened"
                        },
                        "home_services":
                        {
                            "type": "flattened"
                        },
                        "business_services":
                        {
                            "type": "flattened"
                        },
                        "legal_services_government":
                        {
                            "type": "flattened"
                        },
                        "public_local_services":
                        {
                            "type": "flattened"
                        },
                        "shopping_fashion":
                        {
                            "type": "flattened"
                        },
                        "sports":
                        {
                            "type": "flattened"
                        },
                        "travel_vacation":
                        {
                            "type": "flattened"
                        },
                        "vehicles_transportation":
                        {
                            "type": "flattened"
                        }
                    }
                }
            }
        }
        """