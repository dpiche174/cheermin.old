<?php

require_once(__DIR__ . '/addressbook_backend.php');

/**
 * Sample plugin to add a new address book with just a static list of contacts.
 *
 * @license GNU GPLv3+
 * @author Dave Piché
 */
class cheermin extends rcube_plugin {
    private $book;
    private $book_id = 'cheermin';
    private $book_name = 'Cheermin';

    public function init() {
        $this->book = new cheermin_addressbook($this->book_name);

        $this->add_hook('addressbooks_list', array($this, 'address_sources'));
        $this->add_hook('addressbook_get', array($this, 'get_address_book'));

        // Use this address book for autocompletion queries
        // (maybe this should be configurable by the user?).
        $config = rcmail::get_instance()->config;
        $sources = (array) $config->get('autocomplete_addressbooks', array('sql'));
        if (!in_array($this->book_id, $sources)) {
            $sources[] = $this->book_id;
            $config->set('autocomplete_addressbooks', $sources);
        }
    }

    public function address_sources($data) {
        $data['sources'][$this->book_id] = array(
            'id' => $this->book_id,
            'name' => $this->book_name,
            'readonly' => $this->book->readonly,
            'groups' => $this->book->groups,
        );
        return $data;
    }

    public function get_address_book($data) {
        if ($data['id'] === $this->book_id) {
            $data['instance'] = $this->book;
        }
        return $data;
    }
}
