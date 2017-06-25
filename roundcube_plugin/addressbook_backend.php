<?php

/**
 * Example backend class for a custom address book
 *
 * This one just holds a static list of address records
 *
 * @author Dave Piché
 */
class cheermin_addressbook extends rcube_addressbook {
    public $primary_key   = 'ID';
    public $groups        = true;
    public $readonly      = true;
    public $ready         = true;

    private $filter;
    private $result;
    private $name;

    public function __construct($name) {
        $this->name = $name;
    }

    /**
     * Returns addressbook name (e.g. for addressbooks listing)
     */
    public function get_name() {
        return $this->name;
    }

    /**
     * Save a search string for future listings
     *
     * @param mixed $filter Search params to use in listing method, obtained by get_search_set()
     */
    public function set_search_set($filter) {
        $this->filter = $filter;
    }

    /**
     * Getter for saved search properties
     *
     * @return mixed Search properties used by this class
     */
    public function get_search_set() {
        return $this->filter;
    }

    /**
     * Setter for the current group
     * (empty, has to be re-implemented by extending class)
     */
    function set_group($gid) {
        $this->group_id = $gid;
    }

    /**
     * Reset saved results and search parameters
     */
    public function reset() {
        $this->result = null;
        $this->filter = null;
    }

    /**
     * List all active contact groups of this source
     *
     * @param string $search Optional search string to match group name
     * @param int    $mode   Search mode. Sum of self::SEARCH_*
     *
     * @return array  Indexed list of contact groups, each a hash array
     */
    function list_groups($search=null, $mode=0) {
        $command = array(__DIR__ . "/load.py", "groups");

        if ($search) {
            $command[] = sprintf("\"--search=%s\"", $search);
            if ($mode & rcube_addressbook::SEARCH_STRICT) {
                $command[] = "--search-mode=strict";
            }
            else if ($mode & rcube_addressbook::SEARCH_PREFIX) {
                $command[] = "--search-mode=prefix";
            }
        }

        return json_decode(shell_exec(join(" ", $command)), true);
    }

    /**
     * Get group properties such as name and email address(es)
     *
     * @param string $group_id Group identifier
     *
     * @return array Group properties as hash array
     */
    function get_group($group_id) {
        foreach ($this->list_groups() as $group) {
            if ($group['ID'] == $group_id) {
                return $group;
            }
        }
        return null;
    }

    /**
     * List the current set of contact records
     *
     * @param array $cols   List of cols to show
     * @param int   $subset Only return this number of records, use negative values for tail
     *
     * @return array Indexed list of contact records, each a hash array
     */
    public function list_records($cols=null, $subset=0) {
        $records = $this->_list_records();
        $this->result = $this->count();
        foreach ($records as $record) {
            $this->result->add($record);
        }
        return $this->result;
    }

    public function _list_records() {
        if ($this->group_id) {
            $command = sprintf(__DIR__ . "/load.py records --group-id=%s", $this->group_id);
        }
        else {
            $command = sprintf(__DIR__ . "/load.py records");
        }
        return json_decode(shell_exec($command), true);
    }

    /**
     * Search contacts
     *
     * @param mixed   $fields   The field name or array of field names to search in
     * @param mixed   $value    Search value (or array of values when $fields is array)
     * @param int     $mode     Search mode. Sum of rcube_addressbook::SEARCH_*
     * @param boolean $select   True if results are requested, False if count only
     * @param boolean $nocount  True to skip the count query (select only)
     * @param array   $required List of fields that cannot be empty
     *
     * @return object rcube_result_set Contact records and 'count' value
     */
    function search($fields, $value, $mode=0, $select=true, $nocount=false, $required=array()) {
        // todo: No search implemented, just list all records.
        return $this->list_records();
    }

    public function count() {
        $count = count($this->_list_records());
        return new rcube_result_set($count, ($this->list_page - 1) * $this->page_size);
    }

    public function get_result() {
        return $this->result;
    }

    /**
     * Get group assignments of a specific contact record
     *
     * @param mixed $id Record identifier
     *
     * @return array List of assigned groups as ID=>Name pairs
     */
    function get_record_groups($id) {
        return json_decode(shell_exec(sprintf(__DIR__ . "/load.py get_record_groups %s", $id)), true);
    }

    public function get_record($id, $assoc=false) {
        $this->result = null;
        foreach ($this->_list_records() as $record) {
            if ($record['ID'] == $id) {
                $this->result = new rcube_result_set(1);
                $this->result->add($record);
                break;
            }
        }
        return $assoc && $record ? $record : $this->result;
    }
}
