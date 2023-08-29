-- public.availability definition

-- Drop table

-- DROP TABLE public.availability;

CREATE TABLE public.availability (
	"ID" varchar(255) NOT NULL,
	"RouteID" varchar(255) NULL,
	"OriginAirport" varchar(3) NULL,
	"OriginRegion" varchar(255) NULL,
	"DestinationAirport" varchar(3) NULL,
	"DestinationRegion" varchar(255) NULL,
	"NumDaysOut" int4 NULL,
	"Distance" int4 NULL,
	"RouteSource" varchar(255) NULL,
	"Date" date NULL,
	"ParsedDate" timestamp NULL,
	"YAvailable" bool NULL,
	"WAvailable" bool NULL,
	"JAvailable" bool NULL,
	"FAvailable" bool NULL,
	"YMileageCost" varchar(255) NULL,
	"WMileageCost" varchar(255) NULL,
	"JMileageCost" varchar(255) NULL,
	"FMileageCost" varchar(255) NULL,
	"YRemainingSeats" int4 NULL,
	"WRemainingSeats" int4 NULL,
	"JRemainingSeats" int4 NULL,
	"FRemainingSeats" int4 NULL,
	"YAirlines" varchar(255) NULL,
	"WAirlines" varchar(255) NULL,
	"JAirlines" varchar(255) NULL,
	"FAirlines" varchar(255) NULL,
	"YDirect" bool NULL,
	"WDirect" bool NULL,
	"JDirect" bool NULL,
	"FDirect" bool NULL,
	"Source" varchar(255) NULL,
	"ComputedLastSeen" varchar(255) NULL,
	"APITermsOfUse" varchar(255) NULL,
	"AvailabilityTrips" jsonb NULL,
	"CreatedAt" timestamp NULL DEFAULT now(),
	"Route" jsonb NULL,
	CONSTRAINT availability_pkey PRIMARY KEY ("ID")
);
