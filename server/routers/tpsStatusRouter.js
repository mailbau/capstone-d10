const express = require('express');
const tpsStatusController = require('../controllers/tpsstatusController');
const router = express.Router();

// Get all tpsStatus
router.get('/', tpsStatusController.getAllTPSStatus);

// Add tpsStatus
router.post('/', tpsStatusController.addTPSStatus);

// Get specific tpsStatus by ID
router.get('/:tpsStatusId', tpsStatusController.getTPSStatusById);

// Update tpsStatus by ID
router.put('/:tpsStatusId', tpsStatusController.updateTPSStatus);

// Delete tpsStatus by ID
router.delete('/:tpsStatusId', tpsStatusController.deleteTPSStatus);

module.exports = router;