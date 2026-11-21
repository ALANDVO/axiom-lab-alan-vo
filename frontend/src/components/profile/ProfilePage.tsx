import React, { useState, useEffect } from 'react';

interface Skill {
  name: string;
  level: 'beginner' | 'intermediate' | 'advanced';
}

interface Contact {
  type: 'email' | 'phone' | 'github' | 'linkedin';
  value: string;
}

interface ProfileData {
  name: string;
  current_role: string;
  location: string;
  skills: Skill[];
  contacts: Contact[];
  experience: Array<{ title: string; company: string; start: string; end: string }>;
  education: Array<{ degree: string; institution: string; start: string; end: string }>;
  screening_answers: Record<string, string>;
}

const completenessWeights: Record<string, number> = {
  name: 15,
  current_role: 10,
  location: 10,
  skills: 30,
  contacts: 15,
  experience: 15,
  education: 5,
};

export const ProfilePage: React.FC = () => {
  const [data, setData] = useState<ProfileData>({
    name: '',
    current_role: '',
    location: '',
    skills: [],
    contacts: [],
    experience: [],
    education: [],
    screening_answers: {},
  });

  const [dirty, setDirty] = useState(false);
  const [touched, setTouched] = useState<Set<string>>(new Set());

  const handleChange = (e: React.ChangeEvent<any>) => {
    const { name, value } = e.target;
    setData(prev => ({
      ...prev,
      [name]: value === '' ? (name.includes('skills') ? [] : name.includes('experience') ? [] : name.includes('education') ? {} : '') : value,
    }));
    setDirty(true);
  };

  const addSkill = () => {
    setData(prev => ({ ...prev, skills: [...prev.skills, { name: '', level: 'beginner' }] }));
  };

  const removeSkill = (idx: number) => {
    setData(prev => {
      const newSkills = [...prev.skills];
      newSkills.splice(idx, 1);
      return { ...prev, skills: newSkills };
    });
  };

  const addExperience = () => {
    setData(prev => ({ ...prev, experience: [...prev.experience, { title: '', company: '', start: '', end: '' }] }));
  };

  const removeExperience = (idx: number) => {
    setData(prev => {
      const newExp = [...prev.experience];
      newExp.splice(idx, 1);
      return { ...prev, experience: newExp };
    });
  };

  const addEducation = () => {
    setData(prev => ({ ...prev, education: [...prev.education, { degree: '', institution: '', start: '', end: '' }] }));
  };

  const removeEducation = (idx: number) => {
    setData(prev => {
      const newEdu = [...prev.education];
      newEdu.splice(idx, 1);
      return { ...prev, education: newEdu };
    });
  };

  const computeCompleteness = (): number => {
    let filled = 0;
    const total = Object.values(completenessWeights).reduce((a, b) => a + b, 0);

    if (data.name && data.name.trim()) filled += completenessWeights.name;
    if (data.current_role && data.current_role.trim()) filled += completenessWeights.current_role;
    if (data.location && data.location.trim()) filled += completenessWeights.location;
    if (data.skills && data.skills.length > 0) filled += completenessWeights.skills;
    if (data.contacts && data.contacts.length > 0) filled += completenessWeights.contacts;
    if (data.experience && data.experience.length > 0) filled += completenessWeights.experience;
    if (data.education && data.education.length > 0) filled += completenessWeights.education;

    return Math.round((filled / total) * 100);
  };

  const completeness = computeCompleteness();

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>Candidate Profile</h1>

      <div style={{ border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.5rem', marginBottom: '2rem' }}>
        <h2 style={{ marginTop: 0, marginBottom: '1rem' }}>Profile Completeness: <span style={{ color: '#eab308' }}>{completeness}%</span></h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <span style={{ background: '#e2e8f0', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem' }}>
            Name {'='.repeat(data.name?.trim ? (data.name.trim() ? 1 : 0) : 0)}
          </span>
          <span style={{ background: '#e2e8f0', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem' }}>
            Role {'='.repeat(data.current_role?.trim ? (data.current_role.trim() ? 1 : 0) : 0)}
          </span>
          <span style={{ background: '#e2e8f0', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem' }}>
            Location {'='.repeat(data.location?.trim ? (data.location.trim() ? 1 : 0) : 0)}
          </span>
        </div>
        <div style={{ marginTop: '0.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {completeness >= 80 && (
            <span style={{ background: '#22c55e', color: 'white', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem' }}>
              Good progress
            </span>
          )}
          {completeness >= 50 && (
            <span style={{ background: '#f59e0b', color: 'white', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem' }}>
              Halfway there
            </span>
          )}
          {completeness < 50 && (
            <span style={{ background: '#ef4444', color: 'white', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem' }}>
              Start filling
            </span>
          )}
        </div>
      </div>

      {/* Profile Section */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3>Profile</h3>
        <label>
          Name
          <input
            type="text"
            name="name"
            value={data.name || ''}
            onChange={handleChange}
            placeholder="e.g. Alan Vo"
            style={{ width: '100%', padding: '0.5rem', marginBottom: '0.5rem' }}
          />
        </label>
        <label>
          Current Role
          <input
            type="text"
            name="current_role"
            value={data.current_role || ''}
            onChange={handleChange}
            placeholder="e.g. Software Engineer"
            style={{ width: '100%', padding: '0.5rem', marginBottom: '0.5rem' }}
          />
        </label>
        <label>
          Location
          <input
            type="text"
            name="location"
            value={data.location || ''}
            onChange={handleChange}
            placeholder="e.g. San Francisco, CA"
            style={{ width: '100%', padding: '0.5rem', marginBottom: '1rem' }}
          />
        </label>
      </div>

      {/* Skills Section */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3>Skills</h3>
        {data.skills.length > 0 ? (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {data.skills.map((skill, idx) => (
              <li key={idx} style={{ display: 'flex', gap: '0.5rem', alignItems: 'baseline' }}>
                <input
                  type="text"
                  name={`skill_${idx}_name`}
                  value={skill.name || ''}
                  onChange={e => {
                    setData(prev => ({
                      ...prev,
                      skills: prev.skills.map((s, i) =>
                        i === idx ? { ...s, name: e.target.value } : s
                      ),
                    }));
                  }}
                  style={{ flex: 1, padding: '0.5rem', marginRight: '0.5rem' }}
                />
                <select
                  value={skill.level || 'beginner'}
                  onChange={e => {
                    setData(prev => ({
                      ...prev,
                      skills: prev.skills.map((s, i) =>
                        i === idx ? { ...s, level: e.target.value } : s
                      ),
                    }));
                  }}
                  style={{ padding: '0.5rem' }}
                >
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
                <button
                  onClick={() => removeSkill(idx)}
                  style={{ padding: '0.5rem 0.75rem', marginLeft: '0.5rem' }}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ margin: '0.5rem 0' }}>No skills added yet.</p>
        )}
        <button
          onClick={addSkill}
          style={{ marginBottom: '0.5rem', padding: '0.5rem 0.75rem' }}
        >
          Add Skill
        </button>
      </div>

      {/* Contacts Section */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3>Contacts</h3>
        {data.contacts.length > 0 ? (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {data.contacts.map((contact, idx) => (
              <li key={idx} style={{ marginBottom: '0.5rem', padding: '0.5rem', background: '#f1f5f9', borderRadius: '4px' }}>
                <span style={{ fontWeight: 'bold', marginRight: '0.5rem' }}>{contact.type}:</span> {contact.value}
                <button
                  onClick={() => removeContact(idx)}
                  style={{ float: 'right', padding: '0.2rem 0.5rem', fontSize: '0.7rem' }}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ margin: '0.5rem 0' }}>No contacts added yet.</p>
        )}
        <div style={{ display: 'grid', gap: '0.5rem', marginTop: '0.5rem' }}>
          <select
            name="contact_type"
            onChange={e => setData(prev => ({ ...prev, contacts: [...prev.contacts, { type: e.target.value as any, value: '' }] }))}
            style={{ padding: '0.5rem' }}
          >
            <option value="email">Email</option>
            <option value="phone">Phone</option>
            <option value="github">GitHub</option>
            <option value="linkedin">LinkedIn</option>
          </select>
          <input
            type="text"
            name="contact_value"
            value=""
            onChange={e => {
              const type = (e.target as HTMLSelectElement).value as any;
              setData(prev => ({
                ...prev,
                contacts: prev.contacts.map(c =>
                  c.type === type ? { ...c, value: e.target.value } : c
                ),
              }));
            }}
            placeholder="e.g. alanvo@gmail.com"
            style={{ padding: '0.5rem' }}
          />
        </div>
      </div>

      {/* Experience Section */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3>Experience</h3>
        {data.experience.length > 0 ? (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {data.experience.map((exp, idx) => (
              <li key={idx} style={{ marginBottom: '0.75rem', padding: '0.5rem', background: '#f1f5f9', borderRadius: '4px' }}>
                <div style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>{exp.title} at {exp.company}</div>
                <div>{exp.start} – {exp.end || 'Present'}</div>
                <button
                  onClick={() => removeExperience(idx)}
                  style={{ float: 'right', padding: '0.2rem 0.5rem', fontSize: '0.7rem', color: '#ef4444' }}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ margin: '0.5rem 0' }}>No experience added yet.</p>
        )}
        <button onClick={addExperience} style={{ padding: '0.5rem 0.75rem' }}>
          Add Experience
        </button>
      </div>

      {/* Education Section */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3>Education</h3>
        {data.education.length > 0 ? (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {data.education.map((edu, idx) => (
              <li key={idx} style={{ marginBottom: '0.75rem', padding: '0.5rem', background: '#f1f5f9', borderRadius: '4px' }}>
                <div>{edu.degree} – {edu.institution}</div>
                <div>{edu.start} – {edu.end || 'Present'}</div>
                <button
                  onClick={() => removeEducation(idx)}
                  style={{ float: 'right', padding: '0.2rem 0.5rem', fontSize: '0.7rem', color: '#ef4444' }}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ margin: '0.5rem 0' }}>No education added yet.</p>
        )}
        <button onClick={addEducation} style={{ padding: '0.5rem 0.75rem' }}>
          Add Education
        </button>
      </div>

      {/* Screening Section */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3>Screening</h3>
        {Object.keys(data.screening_answers).length > 0 ? (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {Object.entries(data.screening_answers).map(([key, value], idx) => (
              <li key={idx} style={{ marginBottom: '0.5rem', padding: '0.5rem', background: '#f1f5f9', borderRadius: '4px' }}>
                <strong>{key}:</strong> {value}
                <button
                  onClick={() => removeScreeningAnswer(key)}
                  style={{ float: 'right', padding: '0.2rem 0.5rem', fontSize: '0.7rem', color: '#ef4444' }}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ margin: '0.5rem 0' }}>No screening answers yet.</p>
        )}
        <div style={{ display: 'grid', gap: '0.5rem', marginTop: '0.5rem' }}>
          <select
            name="screening_question"
            onChange={e => setData(prev => ({
              ...prev,
              screening_answers: { ...prev.screening_answers, [e.target.value]: '' },
            }))}
            style={{ padding: '0.5rem' }}
          >
            <option value="availability">Availability</option>
            <option value="salary_expectations">Salary Expectations</option>
            <option value="notice_period">Notice Period</option>
            <option value="remote_work">Remote Work Preference</option>
          </select>
          <input
            type="text"
            name="screening_answer"
            value=""
            onChange={e => {
              const question = (e.target as HTMLSelectElement).value;
              setData(prev => ({
                ...prev,
                screening_answers: { ...prev.screening_answers, question: e.target.value },
              }));
            }}
            placeholder="Your answer"
            style={{ padding: '0.5rem' }}
          />
        </div>
      </div>

      {/* Settings Section */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3>Settings</h3>
        <label>
          Notify me about new matching jobs
          <input
            type="checkbox"
            name="notify_new_jobs"
            checked={data.screening_answers.notify_new_jobs === 'yes'}
            onChange={e => setData(prev => ({
              ...prev,
              screening_answers: { ...prev.screening_answers, notify_new_jobs: e.target.checked ? 'yes' : 'no' },
            }))}
            style={{ transform: 'scale(1.2)', marginRight: '0.5rem' }}
          />
        </label>
      </div>

      <div style={{ textAlign: 'right', marginTop: '2rem' }}>
        <button
          onClick={() => {
            // Simulate save - in real app would call API
            setDirty(false);
            alert('Profile saved!');
          }}
          style={{ background: '#3b82f6', color: 'white', padding: '0.75rem 1.5rem', borderRadius: '4px', border: 'none' }}
          disabled={!dirty}
        >
          Save Profile
        </button>
      </div>
    </div>
  );
};
