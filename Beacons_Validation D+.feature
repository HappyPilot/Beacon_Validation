Feature: D+ Beacons Validation

Scenario: Pars CSV and creat full data list
    Given Parsing csv
    Then Create url data list https://beacons.digital.disneyadvertising.com


  Scenario Outline: Pars CSV and creat full data list
    Given Parsing csv
    Then Create full data list <param>
    Examples:for this code
      |param                |
      |event-type           |
      |is-empty             |
      |ad-request-id        |
      |publisher            |
      |ad-fill-id           |
      |account-id           |
      |line-item-id         |
      |ad-id                |
      |device-id            |
      |brand-id             |
      |line-item-ad-product |
      |live                 |
      |event-sub-class      |
      |playback-session-id  |
      |ad-offset-ms          |

  Scenario: 3p Beacons Check
    Given 3p beacons check