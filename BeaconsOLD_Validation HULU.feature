Feature: Beacons Validation

Scenario: Pars CSV and creat full data list
    Given Parsing csv
    Then Create url data list https://t2.hulu.com/v3

  Scenario Outline: Pars CSV and creat full data list
    Given Parsing csv
    Then Create full data list <param>
    Examples:for this code
      |param|
      |app_version    |
      |appversion     |
      |device_ad_id   |
      |device_fam     |
      |device_man     |
      |device_model   |
      |device_platform|
      |device_product |
      |deviceid       |
      |distroplatform |
      |os             |
      |player         |
      |client         |
      |computerguid   |
      |sessionguid    |
      |adposition     |
      |watched        |
      |seq            |
      |placementid    |
      |pod            |
      |stream_type    |
      |source         |
      |assetimpression |
      |timedout       |
      |choiceposition |
      |contentid      |
      |type           |
      |content        |
      |adunit_id      |
      |ts             |
      |alttextintended|
      |alttextshown   |
      |collectionid   |
      |position       |
      |duration       |
      |adplaybackstate|
      |srcclickstate  |
      |src            |