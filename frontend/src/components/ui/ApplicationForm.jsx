'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/Cards';

export default function ApplicationForm({ onClose, onSubmit, initialData }) {
  const [formData, setFormData] = useState({
    code: initialData?.code || '',
    name: initialData?.name || '',
    source: initialData?.source || 'SAP',
    owner: initialData?.owner || '',
    techLead: initialData?.techLead || '',
    criticality: initialData?.criticality || 'Moyenne',
    iamStatus: initialData?.iamStatus || '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.code || !formData.name || !formData.owner || !formData.techLead) {
      alert('Veuillez remplir tous les champs obligatoires.');
      return;
    }

    const appToSave = {
      id: initialData ? initialData.id : formData.code, // keep same ID when editing
      code: formData.code,
      name: formData.name,
      description: initialData?.description || '',
      source: formData.source,
      owner: formData.owner,
      techLead: formData.techLead,
      criticality: formData.criticality,
      iamStatus: formData.iamStatus || 'Non défini',
      category: initialData?.category || 'Nouvelle',
    };

    onSubmit(appToSave);
  };

  return (
    <div className="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-slate-800">
            {initialData ? 'Modifier l\'application' : 'Ajouter une application'}
          </h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 text-2xl leading-none"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Code <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="code"
                value={formData.code}
                onChange={handleChange}
                placeholder="Ex: APP-001"
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Nom <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Ex: Gestion des stocks"
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Source
              </label>
              <select
                name="source"
                value={formData.source}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="SAP">SAP</option>
                <option value="Apple">Apple</option>
                <option value="ServiceNow">ServiceNow</option>
                <option value="HelpDesk">HelpDesk</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Responsable <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="owner"
                value={formData.owner}
                onChange={handleChange}
                placeholder="Nom du responsable"
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Tech Lead <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="techLead"
                value={formData.techLead}
                onChange={handleChange}
                placeholder="Nom du tech lead"
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Criticité
              </label>
              <select
                name="criticality"
                value={formData.criticality}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="Critique">Critique</option>
                <option value="Élevée">Élevée</option>
                <option value="Moyenne">Moyenne</option>
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                IAM / Access
              </label>
              <input
                type="text"
                name="iamStatus"
                value={formData.iamStatus}
                onChange={handleChange}
                placeholder="Ex: SSO, MFA, RBAC..."
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors"
            >
              {initialData ? 'Mettre à jour' : 'Enregistrer'}
            </button>
          </div>
        </form>
      </Card>
    </div>
  );
}